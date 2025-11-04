# SSH Connection Manager

A secure, cross-platform tool to manage SSH credentials and easily connect to your computers around the house.

## Features

- **Secure Storage**: All credentials are encrypted using industry-standard encryption (Fernet with PBKDF2)
- **Master Password Protection**: One password to access all your SSH connections
- **Cross-Platform**: Works on Windows (with PuTTY), macOS, and Linux
- **Easy Management**: Add, edit, delete, and list connections with a simple CLI menu
- **Quick Connect**: Connect to any saved host with just a name
- **Backup Support**: Export your connections for backup purposes

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Optional: Install sshpass (for automatic password authentication on Unix/Linux/macOS)

**On macOS:**
```bash
brew install sshpass
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install sshpass
```

**On Windows:**
PuTTY will be used automatically if installed, or standard SSH client.

## Usage

### Running the Application

```bash
python ssh_manager.py
```

Or make it executable (Unix/Linux/macOS):

```bash
chmod +x ssh_manager.py
./ssh_manager.py
```

### First Time Setup

On first run, you'll be prompted to create a master password. This password protects all your SSH credentials.

**Important:**
- Choose a strong master password
- Don't forget it! There's no recovery mechanism
- Minimum 8 characters required

### Main Menu Options

```
1. Add new connection      - Save a new SSH host with credentials
2. List all connections    - View all saved connections
3. Connect to SSH host     - Connect to a saved host
4. Edit connection         - Modify existing connection details
5. Delete connection       - Remove a saved connection
6. Export connections      - Backup connections to JSON file
7. Exit                    - Close the application
```

### Adding a Connection

1. Select option 1 from the main menu
2. Enter the following information:
   - **Connection name**: A friendly name (e.g., "living-room-pc")
   - **IP address or hostname**: The host to connect to (e.g., "192.168.1.100")
   - **Username**: Your SSH username
   - **Password**: (Optional) Your SSH password
   - **Port**: SSH port (default: 22)
   - **Description**: (Optional) Notes about this connection

Example:
```
Connection name: living-room-pc
IP address: 192.168.1.100
Username: john
Password: ******
Port: 22
Description: Main computer in living room
```

### Connecting to a Host

1. Select option 3 from the main menu
2. Enter the connection name
3. The application will:
   - **On Windows**: Launch PuTTY if available, otherwise use SSH
   - **On macOS/Linux**: Use the terminal SSH client
   - Automatically pass credentials if password is saved

### Security Features

- **Encryption**: All passwords are encrypted using Fernet (AES-128)
- **Key Derivation**: Master password is strengthened using PBKDF2 with 100,000 iterations
- **File Permissions**: Configuration files are protected with restrictive permissions (Unix/Linux/macOS)
- **No Plain Text**: Passwords are never stored in plain text
- **Memory Safe**: Passwords are cleared from memory after use

## File Locations

The application stores encrypted data in:
- **Unix/Linux/macOS**: `~/.ssh_manager/`
- **Windows**: `C:\Users\<username>\.ssh_manager\`

Files created:
- `connections.enc` - Encrypted connection data
- `key.key` - Derived encryption key
- `salt.key` - Salt for key derivation

**Do not delete these files unless you want to reset the application.**

## Examples

### Quick Setup for Multiple Computers

```
Computer 1 (Living Room):
Name: living-room
Host: 192.168.1.100
User: john
Password: mypassword123
Port: 22

Computer 2 (Bedroom):
Name: bedroom-pc
Host: 192.168.1.101
User: john
Password: mypassword123
Port: 22

Computer 3 (Garage Raspberry Pi):
Name: garage-pi
Host: 192.168.1.50
User: pi
Password: raspberry
Port: 22
```

### Connecting to a Saved Host

```bash
# Run the application
python ssh_manager.py

# Select option 3 (Connect to SSH host)
# Enter: living-room
# SSH connection opens automatically!
```

## Troubleshooting

### "Cannot find PuTTY" on Windows

If PuTTY is not found:
1. Download PuTTY from https://www.putty.org/
2. Install it to the default location
3. Or add PuTTY to your PATH environment variable

### "sshpass not found" on macOS/Linux

This is optional. If not installed:
- You'll be prompted to enter the password manually when connecting
- Install sshpass for automatic password authentication (see Installation section)

### Forgot Master Password

Unfortunately, there's no recovery mechanism. If you forget your master password:
1. Delete the `~/.ssh_manager/` directory
2. Restart the application to create a new master password
3. Re-add all your connections

### Connection Timeout

If you can't connect:
- Verify the IP address is correct
- Ensure the computer is powered on and connected to the network
- Check that SSH is enabled on the target computer
- Verify the port number (default is 22)

## Security Best Practices

1. **Use Key-Based Authentication**: For better security, set up SSH keys instead of passwords
2. **Regular Backups**: Use option 6 to export connections regularly
3. **Strong Master Password**: Use a unique, strong master password
4. **Secure Backups**: Keep backup files in a secure location
5. **Network Security**: Use this tool only on trusted networks

## Advanced Usage

### Using with SSH Keys

If you've set up SSH key-based authentication:
1. Add the connection without a password (press Enter when prompted)
2. The SSH client will use your SSH keys automatically

### Custom SSH Ports

If your SSH server uses a non-standard port:
1. Specify the port when adding the connection
2. Example: Port 2222 instead of 22

### Export for Backup

```bash
# Select option 6
# Enter filename: backup.json
# Keep this file secure - it contains your encrypted passwords!
```

## Platform Support

- **Windows 10/11**: Full support with PuTTY or OpenSSH
- **macOS**: All versions with built-in SSH
- **Linux**: All distributions with SSH client
- **Raspberry Pi**: Full support

## Contributing

This is a personal tool, but feel free to modify and extend it for your needs!

## License

Free to use and modify for personal use.

## Support

For issues or questions, refer to this README or modify the code to suit your needs.

---

**Remember**: Keep your master password secure and never share your connection backup files!
