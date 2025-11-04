# macOS Setup Guide

## Prerequisites

### 1. Python 3 (Usually Already Installed)

macOS usually comes with Python, but you may need Python 3.

Check if you have Python 3:
```bash
python3 --version
```

If not installed, you have two options:

**Option A - Official Python:**
Download from: https://www.python.org/downloads/

**Option B - Homebrew (Recommended):**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3
brew install python3
```

### 2. SSH (Already Built-in!)

macOS comes with SSH built-in, so you're ready to go!

## Installation Steps

### Step 1: Download/Clone the Repository

Place the SSH Manager files in a folder, for example:
```
~/Applications/SSH-Manager/
```

Or your Documents folder:
```
~/Documents/SSH-Manager/
```

### Step 2: Install Dependencies

Open Terminal and navigate to the folder:

```bash
cd ~/Documents/SSH-Manager
pip3 install -r requirements.txt
```

## Running the Application

### Method 1: Double-Click .command File (EASIEST!)

Just **double-click `ssh_manager.command`** - that's it!

The first time you double-click:
1. You may see "Cannot be opened because it is from an unidentified developer"
2. Right-click (or Control-click) on `ssh_manager.command`
3. Select "Open"
4. Click "Open" in the dialog
5. From now on, you can just double-click!

The launcher will:
- Automatically check for Python
- Install dependencies if needed
- Launch the SSH Manager
- Open in a Terminal window

### Method 2: Terminal

```bash
cd ~/Documents/SSH-Manager
python3 ssh_manager.py
```

Or make it simpler:
```bash
cd ~/Documents/SSH-Manager
./ssh_manager.py
```

### Method 3: Create Application Bundle (Advanced)

You can create a proper macOS app:

1. Open **Automator** (in Applications)
2. Create new "Application"
3. Add "Run Shell Script" action
4. Paste:
   ```bash
   cd ~/Documents/SSH-Manager
   python3 ssh_manager.py
   ```
5. File → Save as "SSH Manager" to Applications folder
6. Now it appears in Launchpad and Spotlight!

### Method 4: Add to Dock

Drag `ssh_manager.command` to your Dock for one-click access!

### Method 5: Run from Anywhere (Advanced)

Add an alias to your shell profile:

**For bash (older macOS):**
```bash
echo 'alias sshm="python3 ~/Documents/SSH-Manager/ssh_manager.py"' >> ~/.bash_profile
source ~/.bash_profile
```

**For zsh (macOS Catalina and newer):**
```bash
echo 'alias sshm="python3 ~/Documents/SSH-Manager/ssh_manager.py"' >> ~/.zshrc
source ~/.zshrc
```

Now you can run from anywhere:
```bash
sshm
```

## First Run

When you run it for the first time:

1. You'll be asked to create a **Master Password**
2. Choose a strong password (minimum 8 characters)
3. **Remember this password!** You'll need it every time

## Using with Terminal

The app automatically uses macOS Terminal for SSH connections:
- Opens new Terminal window/tab
- Connects automatically
- Passes credentials securely

### Optional: Install sshpass for Auto-Password Entry

By default, you'll need to type the password when connecting. To automate this:

```bash
brew install hudochenkov/sshpass/sshpass
```

Now passwords will be entered automatically!

## Quick Example

```
1. Double-click ssh_manager.command
2. Enter your master password (first time: create one)
3. Select option 1 (Add new connection)
4. Add your computer:
   - Name: home-server
   - IP: 192.168.1.100
   - Username: yourname
   - Password: yourpassword
   - Port: 22
5. Select option 3 (Connect)
6. Enter: home-server
7. Terminal opens and connects!
```

## Troubleshooting

### "Permission denied" when running

Make the script executable:
```bash
cd ~/Documents/SSH-Manager
chmod +x ssh_manager.py
chmod +x ssh_manager.command
```

### "Cannot be opened because it is from an unidentified developer"

Right-click → Open (first time only)

Or disable Gatekeeper temporarily:
```bash
sudo spctl --master-disable
# Open the app
sudo spctl --master-enable
```

### "python3: command not found"

Install Python 3:
```bash
brew install python3
```

### "pip3: command not found"

Try:
```bash
python3 -m pip install -r requirements.txt
```

### Script exits immediately

Use the `.command` file instead, it keeps the Terminal window open.

## Security on macOS

Your encrypted credentials are stored in:
```
~/.ssh_manager/
```

Files:
- `connections.enc` - Encrypted connection data
- `key.key` - Encryption key
- `salt.key` - Key derivation salt

**Keep these files safe!** Don't delete unless you want to reset everything.

File permissions are automatically set to 700 (owner only).

## Backup Your Connections

Regularly backup using option 6 in the menu:
```
Select option: 6
Enter filename: ~/Documents/ssh_backup.json
```

Keep this backup file secure!

## Tips for macOS Users

### 1. Add to Launchpad

Create an Automator app (Method 3 above) for Launchpad access.

### 2. Keyboard Shortcut

Use Automator + System Preferences → Keyboard → Shortcuts to assign a hotkey.

### 3. Dock Access

Drag `ssh_manager.command` to the right side of the Dock (before Trash).

### 4. Spotlight Access

If you create an Automator app, you can launch with Spotlight (⌘ + Space).

### 5. Custom Icon

Download an SSH icon and:
1. Right-click the `.command` file → Get Info
2. Drag an icon file onto the icon in the top-left
3. Now it looks professional!

### 6. iTerm2 Integration

If you use iTerm2 instead of Terminal:
1. iTerm2 → Preferences → General → Magic
2. Enable "Applications in terminal may access clipboard"
3. Better paste and clipboard support!

## Recommended Folder Structure

```
~/Documents/SSH-Manager/          <- Installation folder
├── ssh_manager.py                <- Main application
├── ssh_manager.command           <- Double-click to run
├── requirements.txt
├── README.md
└── QUICKSTART.md

~/.ssh_manager/                   <- Data folder (auto-created)
├── connections.enc
├── key.key
└── salt.key

~/Documents/                      <- Backups
└── ssh_backup.json
```

## Integration with macOS Keychain (Future Enhancement)

While the app currently uses its own encryption, you could integrate with macOS Keychain for system-level password management. This would require modifying the code to use the `keyring` Python library.

## Using SSH Keys Instead of Passwords

For better security, consider using SSH keys:

1. Generate SSH key pair:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copy public key to remote server:
   ```bash
   ssh-copy-id username@192.168.1.100
   ```

3. In SSH Manager, add connection WITHOUT password
4. SSH will use your key automatically!

## Bonus: Create a Native macOS App Icon

**Quick Custom Icon:**
1. Find an SSH icon online (PNG/ICNS format)
2. Right-click `ssh_manager.command` → Get Info
3. Drag icon file to the small icon in top-left corner
4. Close Info window
5. Your app now has a custom icon!

**Professional ICNS File:**
Use the `iconutil` command to create professional macOS icons from PNG files.

## Uninstalling

To completely remove:

```bash
# Remove application files
rm -rf ~/Documents/SSH-Manager

# Remove data (⚠️ Deletes all saved connections!)
rm -rf ~/.ssh_manager

# Remove alias (if you added one)
# Edit ~/.zshrc or ~/.bash_profile and remove the alias line
```

## Privacy & Security Notes

- All data stays local on your Mac
- No internet connection required (except for SSH connections)
- Credentials never leave your computer
- Uses standard cryptography libraries
- File permissions restrict access to your user account only

## Need Help?

Check the main README.md for detailed documentation!

---

## Quick Reference Commands

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run application
python3 ssh_manager.py

# Make executable
chmod +x ssh_manager.py

# Install sshpass (optional)
brew install hudochenkov/sshpass/sshpass

# Create alias (zsh)
echo 'alias sshm="python3 ~/Documents/SSH-Manager/ssh_manager.py"' >> ~/.zshrc
source ~/.zshrc
```

Enjoy your SSH Connection Manager on macOS! 🍎
