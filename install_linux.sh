#!/bin/bash
# Ransomware Canary - Linux Installation Script
# This script configures auto-start, password-less execution, and desktop icon
# Run as: sudo bash install_linux.sh

# 1. Get the current directory and user
APP_DIR=$(pwd)
CURRENT_USER=$(logname)

# Check if binary exists (preferred) or fall back to Python script
BINARY_PATH="$APP_DIR/dist/RansomwareCanary"
PYTHON_BIN="$APP_DIR/venv/bin/python3"
SCRIPT_PATH="$APP_DIR/main_gui.py"

# Determine which method to use
if [ -f "$BINARY_PATH" ]; then
    echo "[*] Using compiled binary: $BINARY_PATH"
    EXECUTABLE="$BINARY_PATH"
    USE_BINARY=true
    # Make the file executable (just in case)
    chmod +x "$BINARY_PATH"
elif [ -f "$PYTHON_BIN" ] && [ -f "$SCRIPT_PATH" ]; then
    echo "[*] Binary not found. Using Python script: $SCRIPT_PATH"
    EXECUTABLE="$PYTHON_BIN $SCRIPT_PATH"
    USE_BINARY=false
else
    echo "[-] ERROR: Neither binary nor Python script found!"
    echo "[-] Binary path: $BINARY_PATH"
    echo "[-] Python path: $PYTHON_BIN"
    echo "[-] Script path: $SCRIPT_PATH"
    exit 1
fi

echo "[*] Installing Ransomware Canary for user: $CURRENT_USER..."

# 2. Configure Password-less Root Access (SUDOERS)
echo "[*] Configuring Password-less Root Access for the Canary..."

if [ "$USE_BINARY" = true ]; then
    # Whitelist the binary
    echo "$CURRENT_USER ALL=(root) NOPASSWD: $BINARY_PATH" | sudo tee /etc/sudoers.d/ransomware_canary > /dev/null
else
    # Whitelist the Python script
    echo "$CURRENT_USER ALL=(root) NOPASSWD: $PYTHON_BIN $SCRIPT_PATH" | sudo tee /etc/sudoers.d/ransomware_canary > /dev/null
fi

sudo chmod 0440 /etc/sudoers.d/ransomware_canary

# 3. Create Desktop Shortcut (The Icon)
echo "[*] Creating Desktop Icon..."

cat <<EOF > /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop
[Desktop Entry]
Type=Application
Name=Ransomware Canary
Comment=Active Defense System - Zero-Infrastructure Endpoint Protection
Exec=sudo $EXECUTABLE
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
if [ "$USE_BINARY" = true ]; then
    echo "The app is installed as a standalone binary (no Python required)."
else
    echo "The app is installed using Python script."
    echo "To build a binary, run: ./venv/bin/pyinstaller --onefile --windowed --name=\"RansomwareCanary\" --hidden-import=pystray --hidden-import=PIL main_gui.py"
fi
echo ""
echo "1. An icon is now on the Desktop."
echo "2. The app will Auto-Start every time the PC turns on."
echo "3. No password will be required to run it."
echo ""
echo "To test: Reboot your computer and check the system tray."
echo "====================================================="
