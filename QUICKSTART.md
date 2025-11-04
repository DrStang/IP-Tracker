# Quick Start Guide

Get up and running with SSH Connection Manager in 5 minutes!

## Step 1: Install

```bash
# Install dependencies
pip install -r requirements.txt
```

## Step 2: Run

```bash
# Make executable (optional, Unix/Linux/macOS only)
chmod +x ssh_manager.py

# Run the application
python ssh_manager.py
```

## Step 3: First Time Setup

You'll be prompted to create a master password:

```
=== First Time Setup ===
Please create a master password to protect your SSH credentials.
Enter master password: ********
Confirm master password: ********
✓ Master password set successfully!
```

**Remember this password! You'll need it every time you use the tool.**

## Step 4: Add Your First Computer

```
Select option: 1

Connection name: living-room-pc
IP address: 192.168.1.100
Username: yourname
Password: ******
Port: 22
Description: My living room computer

✓ Connection saved!
```

## Step 5: Connect!

```
Select option: 3

Enter connection name: living-room-pc

Connecting to 192.168.1.100...
[SSH session opens]
```

That's it! You're connected!

## Common Connection Examples

### Desktop Computer
```
Name: office-desktop
Host: 192.168.1.100
User: john
Port: 22
```

### Raspberry Pi
```
Name: garage-pi
Host: 192.168.1.50
User: pi
Port: 22
```

### Server with Custom Port
```
Name: web-server
Host: 192.168.1.200
User: admin
Port: 2222
```

### Remote Server (DNS/Domain)
```
Name: cloud-server
Host: server.example.com
User: admin
Port: 22
```

## Tips

1. **Naming**: Use descriptive names like "bedroom-pc" or "garage-pi"
2. **Passwords**: Save passwords for quick access, or leave blank for SSH key auth
3. **Port**: Most SSH servers use port 22 (default)
4. **Backup**: Use option 6 to export connections regularly
5. **Multiple Computers**: Export from one computer, import on another - no need to re-enter!

## Transfer to Another Computer

**On Computer 1:**
```
Select option: 6 (Export)
Enter filename: my_ssh_connections.json
Copy this file to Computer 2 (USB, cloud, etc.)
```

**On Computer 2:**
```
Select option: 7 (Import)
Enter filename: my_ssh_connections.json
Choose: (m)erge or (r)eplace
Done! All your connections are now on Computer 2!
```

## Need Help?

Run the app and explore the menu:
```
1. Add new connection      - Save SSH hosts
2. List all connections    - View saved connections
3. Connect to SSH host     - Quick connect
4. Edit connection         - Update details
5. Delete connection       - Remove a connection
6. Export connections      - Backup to JSON
7. Import connections      - Restore from JSON
8. Exit                    - Quit
```

See README.md for detailed documentation.
