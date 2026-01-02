#!/bin/bash
# Ransomware Canary - Linux Installation Script
# This script configures auto-start, password-less execution, and desktop icon
# Run as: sudo bash install_linux.sh

# 1. Get the current directory and user
APP_DIR=$(pwd)
CURRENT_USER=$(logname)

# Check if launcher script exists
LAUNCHER_PATH="$APP_DIR/launcher.sh"

if [ ! -f "$LAUNCHER_PATH" ]; then
    echo "[-] ERROR: launcher.sh not found!"
    echo "[-] Make sure you're running this from the RansomwareCanary directory"
    exit 1
fi

# Make launcher executable
chmod +x "$LAUNCHER_PATH"

# Check if binary exists (preferred) or fall back to Python script
BINARY_PATH="$APP_DIR/dist/RansomwareCanary"
PYTHON_BIN="$APP_DIR/venv/bin/python3"
SCRIPT_PATH="$APP_DIR/main_gui.py"

# Determine which method to use (for sudoers configuration)
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

# Clean up old sudoers rules first
sudo rm -f /etc/sudoers.d/ransomware_canary

if [ "$USE_BINARY" = true ]; then
    # Whitelist the binary with SETENV permission (for sudo -E)
    echo "$CURRENT_USER ALL=(root) NOPASSWD: SETENV: $BINARY_PATH" | sudo tee /etc/sudoers.d/ransomware_canary > /dev/null
else
    # Whitelist the Python script with SETENV permission
    echo "$CURRENT_USER ALL=(root) NOPASSWD: SETENV: $PYTHON_BIN $SCRIPT_PATH" | sudo tee /etc/sudoers.d/ransomware_canary > /dev/null
fi

sudo chmod 0440 /etc/sudoers.d/ransomware_canary

# 3. Create Application Menu Entry (Start Menu)
echo "[*] Adding to Application Menu..."

# Use absolute path to launcher
LAUNCHER_ABS=$(readlink -f "$LAUNCHER_PATH" || echo "$LAUNCHER_PATH")

# Create .desktop file in application menu directory
mkdir -p /home/$CURRENT_USER/.local/share/applications

cat <<EOF > /home/$CURRENT_USER/.local/share/applications/RansomwareCanary.desktop
[Desktop Entry]
Type=Application
Name=Ransomware Canary
Comment=Active Defense System - Zero-Infrastructure Endpoint Protection
Exec=$LAUNCHER_ABS
Icon=security-high
Terminal=false
Categories=Utility;Security;
X-GNOME-Autostart-enabled=true
EOF

# Make it executable
chmod +x /home/$CURRENT_USER/.local/share/applications/RansomwareCanary.desktop

# CRITICAL: Change ownership of menu file to user
chown $CURRENT_USER:$CURRENT_USER /home/$CURRENT_USER/.local/share/applications/RansomwareCanary.desktop

# Refresh application menu database
sudo -u $CURRENT_USER update-desktop-database /home/$CURRENT_USER/.local/share/applications/ 2>/dev/null || true

# 4. Add to Auto-Start (Runs on Boot)
echo "[*] Adding to Startup Applications..."

mkdir -p /home/$CURRENT_USER/.config/autostart

# Create autostart desktop file with proper settings
cat <<EOF > /home/$CURRENT_USER/.config/autostart/RansomwareCanary.desktop
[Desktop Entry]
Type=Application
Name=Ransomware Canary
Comment=Active Defense System - Zero-Infrastructure Endpoint Protection
Exec=$LAUNCHER_ABS
Icon=security-high
Terminal=false
Categories=Utility;Security;
X-GNOME-Autostart-enabled=true
Hidden=false
NoDisplay=false
EOF

# CRITICAL: Change ownership of autostart file to user
chown $CURRENT_USER:$CURRENT_USER /home/$CURRENT_USER/.config/autostart/RansomwareCanary.desktop

# Make it executable
chmod +x /home/$CURRENT_USER/.config/autostart/RansomwareCanary.desktop

# Trust the autostart file
sudo -u $CURRENT_USER gio set /home/$CURRENT_USER/.config/autostart/RansomwareCanary.desktop metadata::trusted true 2>/dev/null || true

echo "====================================================="
echo "[+] INSTALLATION COMPLETE."
echo ""
if [ "$USE_BINARY" = true ]; then
    echo "The app is installed as a standalone binary (no Python required)."
else
    echo "The app is installed using Python script."
    echo "To build a binary, run: ./venv/bin/pyinstaller --onefile --windowed --name=\"RansomwareCanary\" --hidden-import=pystray --hidden-import=PIL main_gui.py"
fi
echo ""
echo "1. The app is installed in your Application Menu (press Super key, search 'Ransomware')."
echo "2. You can right-click the menu icon and 'Add to Favorites' (Dock) if desired."
echo "3. The app will Auto-Start every time the PC turns on."
echo "4. No password will be required to run it."
echo ""
echo "To test: Reboot your computer and check the system tray."
echo "Or launch manually: Press Super key, type 'Ransomware', and click the icon."
echo "====================================================="
