#!/bin/bash
# Ransomware Canary - Linux Installation Script
# This script configures auto-start, password-less execution, and desktop icon
# Run as: sudo bash install_linux.sh

# 1. Get the current directory and user
APP_DIR=$(pwd)
CURRENT_USER=$(logname)

# Validate we're in the right directory
if [ ! -f "$APP_DIR/main_gui.py" ]; then
    echo "[-] ERROR: main_gui.py not found in current directory."
    echo "[-] Please run this script from the RansomwareCanary folder."
    exit 1
fi

PYTHON_BIN="$APP_DIR/venv/bin/python3"
SCRIPT_PATH="$APP_DIR/main_gui.py"

# Check if venv exists, if not, create it
if [ ! -f "$PYTHON_BIN" ]; then
    echo "[*] Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "[*] Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
fi

echo "[*] Installing Ransomware Canary for user: $CURRENT_USER..."

# 2. Make the app run without asking for a password (SUDOERS)
# This is a standard SysAdmin trick. We tell Linux: "Allow this specific python script to run as root without a password."
echo "[*] Configuring Password-less Root Access for the Canary..."

echo "$CURRENT_USER ALL=(root) NOPASSWD: $PYTHON_BIN $SCRIPT_PATH" | sudo tee /etc/sudoers.d/ransomware_canary > /dev/null
sudo chmod 0440 /etc/sudoers.d/ransomware_canary

# 3. Create a Desktop Shortcut (The Icon)
echo "[*] Creating Desktop Icon..."

cat <<EOF > /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop
[Desktop Entry]
Type=Application
Name=Ransomware Canary
Comment=Active Defense System - Zero-Infrastructure Endpoint Protection
Exec=sudo $PYTHON_BIN $SCRIPT_PATH
Icon=security-high
Terminal=false
Categories=Utility;Security;
EOF

# Make it executable
chmod +x /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop

# Trust the icon (Ubuntu specific)
gio set /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop metadata::trusted true 2>/dev/null || true

# 4. Add to Auto-Start (Runs on Boot)
echo "[*] Adding to Startup Applications..."

mkdir -p /home/$CURRENT_USER/.config/autostart
cp /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop /home/$CURRENT_USER/.config/autostart/

echo "====================================================="
echo "✅ INSTALLATION COMPLETE."
echo ""
echo "1. An icon is now on the Desktop."
echo "2. The app will Auto-Start every time the PC turns on."
echo "3. No password will be required to run it."
echo ""
echo "To test: Reboot your computer and check the system tray."
echo "====================================================="

