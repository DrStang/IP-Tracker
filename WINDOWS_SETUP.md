# Windows Setup Guide

## Prerequisites

### 1. Install Python (if not already installed)

Download Python from: https://www.python.org/downloads/

**Important:** During installation, check "Add Python to PATH"!

To verify Python is installed:
```cmd
python --version
```

### 2. Install PuTTY (Optional but Recommended)

Download from: https://www.putty.org/

Install to default location: `C:\Program Files\PuTTY\`

## Installation Steps

### Step 1: Download/Clone the Repository

Place the SSH Manager files in a folder, for example:
```
C:\Tools\SSH-Manager\
```

### Step 2: Install Dependencies

Open Command Prompt or PowerShell in the SSH Manager folder:

**Method A - Right-click in folder:**
- Hold Shift + Right-click in the folder
- Select "Open PowerShell window here" or "Open Command Prompt here"

**Method B - Navigate manually:**
```cmd
cd C:\Tools\SSH-Manager
```

Then install dependencies:
```cmd
pip install -r requirements.txt
```

## Running the Application

### Method 1: Double-Click Batch File (EASIEST!)

Just double-click `ssh_manager.bat` - that's it!

The batch file will:
- Launch the SSH Manager
- Keep the window open so you can see any messages

### Method 2: Command Prompt / PowerShell

```cmd
cd C:\Tools\SSH-Manager
python ssh_manager.py
```

### Method 3: Create Desktop Shortcut

1. Right-click `ssh_manager.bat`
2. Select "Create shortcut"
3. Drag the shortcut to your Desktop
4. (Optional) Right-click shortcut → Properties → Change Icon

Now you can launch from your Desktop!

### Method 4: Add to Windows Terminal (if you use it)

If you use Windows Terminal, you can add it as a profile:

1. Open Windows Terminal
2. Settings → Add a new profile
3. Command line: `python C:\Tools\SSH-Manager\ssh_manager.py`
4. Name: "SSH Manager"

### Method 5: Run from Anywhere (Advanced)

Add the folder to your PATH:

1. Search Windows for "Environment Variables"
2. Click "Environment Variables"
3. Under "User variables", select "Path"
4. Click "Edit" → "New"
5. Add: `C:\Tools\SSH-Manager`
6. Click OK on all dialogs

Now you can run from any Command Prompt:
```cmd
python ssh_manager.py
```

## First Run

When you run it for the first time:

1. You'll be asked to create a **Master Password**
2. Choose a strong password (minimum 8 characters)
3. **Remember this password!** You'll need it every time

## Using with PuTTY

The app automatically detects PuTTY if installed at:
- `C:\Program Files\PuTTY\putty.exe`
- `C:\Program Files (x86)\PuTTY\putty.exe`

When you connect to a saved host:
- PuTTY window will open automatically
- Credentials are passed automatically
- Just start working!

## Quick Example

```
1. Double-click ssh_manager.bat
2. Enter your master password
3. Select option 1 (Add new connection)
4. Add your computer:
   - Name: home-pc
   - IP: 192.168.1.100
   - Username: yourname
   - Password: yourpassword
   - Port: 22
5. Select option 3 (Connect)
6. Enter: home-pc
7. PuTTY opens and connects!
```

## Troubleshooting

### "python is not recognized"

Python is not installed or not in PATH:
1. Reinstall Python
2. Check "Add Python to PATH" during installation
3. Restart Command Prompt

### "pip is not recognized"

Try:
```cmd
python -m pip install -r requirements.txt
```

### "Cannot find PuTTY"

Either:
- Install PuTTY to default location
- The app will fall back to Windows SSH client (if available)
- Or manually specify PuTTY path in the code

### Script exits immediately

Use the batch file (`ssh_manager.bat`) instead of running directly.
The batch file keeps the window open.

## Security on Windows

Your encrypted credentials are stored in:
```
C:\Users\YourUsername\.ssh_manager\
```

Files:
- `connections.enc` - Encrypted connection data
- `key.key` - Encryption key
- `salt.key` - Key derivation salt

**Keep these files safe!** Don't delete unless you want to reset everything.

## Backup Your Connections

Regularly backup using option 6 in the menu:
```
Select option: 6
Enter filename: C:\Users\YourName\Documents\ssh_backup.json
```

Keep this backup file secure!

## Tips for Windows Users

1. **Pin to Taskbar**: Drag `ssh_manager.bat` to taskbar for one-click access
2. **Startup Folder**: Add shortcut to `shell:startup` to run on boot
3. **Custom Icon**: Download an SSH icon and apply to your shortcut
4. **Windows Terminal**: Add as a profile for modern terminal experience

## Recommended Setup

```
C:\Tools\SSH-Manager\           <- Your installation folder
├── ssh_manager.py              <- Main application
├── ssh_manager.bat             <- Double-click to run
├── requirements.txt
├── README.md
└── QUICKSTART.md

Desktop\
└── SSH Manager.lnk             <- Shortcut for easy access

C:\Users\YourName\.ssh_manager\ <- Data folder (auto-created)
├── connections.enc
├── key.key
└── salt.key
```

## Need Help?

Check the main README.md for detailed documentation!
