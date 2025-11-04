#!/usr/bin/env python3
"""
SSH Connection Manager
A secure tool to manage and connect to SSH hosts with saved credentials
"""

import os
import sys
import json
import platform
import subprocess
import getpass
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class SSHManager:
    def __init__(self):
        self.config_dir = Path.home() / '.ssh_manager'
        self.config_file = self.config_dir / 'connections.enc'
        self.key_file = self.config_dir / 'key.key'
        self.salt_file = self.config_dir / 'salt.key'
        self.fernet = None
        self.initialize()

    def initialize(self):
        """Initialize the configuration directory and encryption"""
        self.config_dir.mkdir(exist_ok=True)

        # Set restrictive permissions on the config directory
        if platform.system() != 'Windows':
            os.chmod(self.config_dir, 0o700)

        if not self.key_file.exists():
            self.setup_master_password()
        else:
            self.unlock_with_master_password()

    def setup_master_password(self):
        """Setup master password for first time use"""
        print("\n=== First Time Setup ===")
        print("Please create a master password to protect your SSH credentials.")

        while True:
            password = getpass.getpass("Enter master password: ")
            confirm = getpass.getpass("Confirm master password: ")

            if password == confirm and len(password) >= 8:
                # Generate salt
                salt = os.urandom(16)
                self.salt_file.write_bytes(salt)

                # Derive key from password
                key = self.derive_key(password, salt)
                self.key_file.write_bytes(key)

                # Set restrictive permissions
                if platform.system() != 'Windows':
                    os.chmod(self.key_file, 0o600)
                    os.chmod(self.salt_file, 0o600)

                self.fernet = Fernet(key)

                # Create empty encrypted connections file
                self.save_connections({})

                print("✓ Master password set successfully!\n")
                break
            elif len(password) < 8:
                print("✗ Password must be at least 8 characters long.\n")
            else:
                print("✗ Passwords do not match. Please try again.\n")

    def unlock_with_master_password(self):
        """Unlock the manager with master password"""
        salt = self.salt_file.read_bytes()

        for attempt in range(3):
            password = getpass.getpass("Enter master password: ")
            key = self.derive_key(password, salt)

            try:
                self.fernet = Fernet(key)
                # Test if the key works
                self.load_connections()
                print("✓ Unlocked successfully!\n")
                return
            except Exception:
                remaining = 2 - attempt
                if remaining > 0:
                    print(f"✗ Incorrect password. {remaining} attempt(s) remaining.\n")
                else:
                    print("✗ Too many failed attempts. Exiting.")
                    sys.exit(1)

    def derive_key(self, password, salt):
        """Derive encryption key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key

    def load_connections(self):
        """Load and decrypt connections"""
        if not self.config_file.exists():
            return {}

        encrypted_data = self.config_file.read_bytes()
        if not encrypted_data:
            return {}

        decrypted_data = self.fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())

    def save_connections(self, connections):
        """Encrypt and save connections"""
        data = json.dumps(connections, indent=2)
        encrypted_data = self.fernet.encrypt(data.encode())
        self.config_file.write_bytes(encrypted_data)

        if platform.system() != 'Windows':
            os.chmod(self.config_file, 0o600)

    def add_connection(self):
        """Add a new SSH connection"""
        print("\n=== Add New Connection ===")

        connections = self.load_connections()

        name = input("Connection name (e.g., 'living-room-pc'): ").strip()
        if not name:
            print("✗ Connection name cannot be empty.")
            return

        if name in connections:
            overwrite = input(f"Connection '{name}' already exists. Overwrite? (y/n): ")
            if overwrite.lower() != 'y':
                print("Operation cancelled.")
                return

        host = input("IP address or hostname: ").strip()
        username = input("Username: ").strip()
        password = getpass.getpass("Password (optional, press Enter to skip): ").strip()
        port = input("Port (default 22): ").strip() or "22"
        description = input("Description (optional): ").strip()

        connections[name] = {
            'host': host,
            'username': username,
            'password': password,
            'port': port,
            'description': description
        }

        self.save_connections(connections)
        print(f"✓ Connection '{name}' saved successfully!\n")

    def list_connections(self):
        """List all saved connections"""
        connections = self.load_connections()

        if not connections:
            print("\nNo saved connections found.")
            print("Use option 1 to add a new connection.\n")
            return

        print("\n=== Saved Connections ===")
        print(f"{'Name':<20} {'Host':<20} {'User':<15} {'Port':<6} {'Description'}")
        print("-" * 80)

        for name, conn in sorted(connections.items()):
            desc = conn.get('description', '')[:30]
            print(f"{name:<20} {conn['host']:<20} {conn['username']:<15} {conn['port']:<6} {desc}")

        print()

    def connect(self):
        """Connect to a saved SSH host"""
        connections = self.load_connections()

        if not connections:
            print("\n✗ No saved connections found.")
            return

        print("\n=== Connect to SSH Host ===")
        self.list_connections()

        name = input("Enter connection name: ").strip()

        if name not in connections:
            print(f"✗ Connection '{name}' not found.")
            return

        conn = connections[name]
        self.establish_connection(conn)

    def establish_connection(self, conn):
        """Establish SSH connection based on OS"""
        system = platform.system()

        if system == 'Windows':
            # Check if PuTTY is available
            putty_paths = [
                r'C:\Program Files\PuTTY\putty.exe',
                r'C:\Program Files (x86)\PuTTY\putty.exe',
                'putty.exe'  # In PATH
            ]

            putty_path = None
            for path in putty_paths:
                if os.path.exists(path) or path == 'putty.exe':
                    putty_path = path
                    break

            if putty_path:
                self.connect_putty(conn, putty_path)
            else:
                self.connect_ssh(conn)
        else:
            # Unix/Linux/macOS
            self.connect_ssh(conn)

    def connect_putty(self, conn, putty_path):
        """Connect using PuTTY on Windows"""
        print(f"\nConnecting to {conn['host']} using PuTTY...")

        cmd = [
            putty_path,
            '-ssh',
            f"{conn['username']}@{conn['host']}",
            '-P', conn['port']
        ]

        if conn.get('password'):
            cmd.extend(['-pw', conn['password']])

        try:
            subprocess.run(cmd)
        except Exception as e:
            print(f"✗ Error launching PuTTY: {e}")
            print("\nTrying standard SSH client instead...")
            self.connect_ssh(conn)

    def connect_ssh(self, conn):
        """Connect using standard SSH client"""
        print(f"\nConnecting to {conn['host']}...")

        if conn.get('password'):
            print("Note: Password is saved. You may be prompted if key authentication fails.")
            # We'll use sshpass if available for password auth
            if self.is_command_available('sshpass'):
                cmd = [
                    'sshpass', '-p', conn['password'],
                    'ssh',
                    '-o', 'StrictHostKeyChecking=no',
                    '-p', conn['port'],
                    f"{conn['username']}@{conn['host']}"
                ]
            else:
                print("Tip: Install 'sshpass' for automatic password authentication")
                print(f"For now, use password: {conn['password']}\n")
                cmd = [
                    'ssh',
                    '-p', conn['port'],
                    f"{conn['username']}@{conn['host']}"
                ]
        else:
            cmd = [
                'ssh',
                '-p', conn['port'],
                f"{conn['username']}@{conn['host']}"
            ]

        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print("\n\nConnection closed.")
        except Exception as e:
            print(f"✗ Error connecting: {e}")

    def is_command_available(self, command):
        """Check if a command is available in PATH"""
        try:
            subprocess.run([command, '--version'],
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            return False

    def delete_connection(self):
        """Delete a saved connection"""
        connections = self.load_connections()

        if not connections:
            print("\n✗ No saved connections found.")
            return

        print("\n=== Delete Connection ===")
        self.list_connections()

        name = input("Enter connection name to delete: ").strip()

        if name not in connections:
            print(f"✗ Connection '{name}' not found.")
            return

        confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ")
        if confirm.lower() == 'y':
            del connections[name]
            self.save_connections(connections)
            print(f"✓ Connection '{name}' deleted successfully!\n")
        else:
            print("Operation cancelled.")

    def edit_connection(self):
        """Edit an existing connection"""
        connections = self.load_connections()

        if not connections:
            print("\n✗ No saved connections found.")
            return

        print("\n=== Edit Connection ===")
        self.list_connections()

        name = input("Enter connection name to edit: ").strip()

        if name not in connections:
            print(f"✗ Connection '{name}' not found.")
            return

        conn = connections[name]
        print(f"\nEditing '{name}' (press Enter to keep current value)")

        host = input(f"IP address [{conn['host']}]: ").strip() or conn['host']
        username = input(f"Username [{conn['username']}]: ").strip() or conn['username']

        change_pw = input("Change password? (y/n): ")
        if change_pw.lower() == 'y':
            password = getpass.getpass("New password (or press Enter to remove): ").strip()
        else:
            password = conn.get('password', '')

        port = input(f"Port [{conn['port']}]: ").strip() or conn['port']
        description = input(f"Description [{conn.get('description', '')}]: ").strip() or conn.get('description', '')

        connections[name] = {
            'host': host,
            'username': username,
            'password': password,
            'port': port,
            'description': description
        }

        self.save_connections(connections)
        print(f"✓ Connection '{name}' updated successfully!\n")

    def export_connections(self):
        """Export connections to a JSON file (passwords will be encrypted)"""
        connections = self.load_connections()

        if not connections:
            print("\n✗ No connections to export.")
            return

        export_file = input("Enter export filename (e.g., backup.json): ").strip()
        if not export_file:
            print("✗ Invalid filename.")
            return

        try:
            with open(export_file, 'w') as f:
                json.dump(connections, f, indent=2)
            print(f"✓ Connections exported to {export_file}")
            print("⚠️  Warning: This file contains passwords. Keep it secure!")
        except Exception as e:
            print(f"✗ Error exporting: {e}")

    def show_menu(self):
        """Display main menu"""
        while True:
            print("\n╔════════════════════════════════════════╗")
            print("║      SSH Connection Manager            ║")
            print("╚════════════════════════════════════════╝")
            print("1. Add new connection")
            print("2. List all connections")
            print("3. Connect to SSH host")
            print("4. Edit connection")
            print("5. Delete connection")
            print("6. Export connections (backup)")
            print("7. Exit")
            print()

            choice = input("Select an option (1-7): ").strip()

            if choice == '1':
                self.add_connection()
            elif choice == '2':
                self.list_connections()
            elif choice == '3':
                self.connect()
            elif choice == '4':
                self.edit_connection()
            elif choice == '5':
                self.delete_connection()
            elif choice == '6':
                self.export_connections()
            elif choice == '7':
                print("\nGoodbye!")
                sys.exit(0)
            else:
                print("✗ Invalid option. Please try again.")

def main():
    """Main entry point"""
    try:
        manager = SSHManager()
        manager.show_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
