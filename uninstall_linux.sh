#!/bin/bash
# Ransomware Canary - Linux Uninstall Script
# This script removes the app, stops all processes, and cleans up all files
# Run as: sudo bash uninstall_linux.sh

# 1. Get the current user
CURRENT_USER=$(logname)

echo "====================================================="
echo "[*] Uninstalling Ransomware Canary..."
echo "====================================================="

# 2. Stop all running processes
echo "[*] Stopping all RansomwareCanary processes..."

# Kill by process name (binary)
pkill -f "RansomwareCanary" 2>/dev/null || true

# Kill by Python script name
pkill -f "main_gui.py" 2>/dev/null || true

# Kill by launcher script
pkill -f "launcher.sh" 2>/dev/null || true

# Give processes a moment to terminate
sleep 1

# Force kill if still running
pkill -9 -f "RansomwareCanary" 2>/dev/null || true
pkill -9 -f "main_gui.py" 2>/dev/null || true

echo "[+] All processes stopped"

# 3. Remove sudoers rule
echo "[*] Removing password-less sudo configuration..."
sudo rm -f /etc/sudoers.d/ransomware_canary
echo "[+] Sudoers rule removed"

# 4. Remove desktop shortcut (if it exists)
echo "[*] Removing desktop shortcut..."
rm -f /home/$CURRENT_USER/Desktop/RansomwareCanary.desktop
echo "[+] Desktop shortcut removed"

# 5. Remove autostart entry
echo "[*] Removing autostart entry..."
rm -f /home/$CURRENT_USER/.config/autostart/RansomwareCanary.desktop
echo "[+] Autostart entry removed"

# 6. Remove application menu entry
echo "[*] Removing application menu entry..."
rm -f /home/$CURRENT_USER/.local/share/applications/RansomwareCanary.desktop

# Refresh application menu database
sudo -u $CURRENT_USER update-desktop-database /home/$CURRENT_USER/.local/share/applications/ 2>/dev/null || true
echo "[+] Application menu entry removed"

# 7. Verify cleanup
echo ""
echo "====================================================="
echo "[+] UNINSTALLATION COMPLETE"
echo "====================================================="
echo ""
echo "Removed:"
echo "  - All running processes"
echo "  - Sudoers configuration"
echo "  - Desktop shortcut"
echo "  - Autostart entry"
echo "  - Application menu entry"
echo ""
echo "Note: The application files in this directory were NOT deleted."
echo "You can reinstall by running: sudo bash install_linux.sh"
echo "====================================================="

