#!/bin/bash
# Ransomware Canary - Release Package Creator
# This script creates a clean release package for distribution

RELEASE_NAME="RansomwareCanary_Linux_Release"
RELEASE_ZIP="RansomwareCanary_Linux_App.zip"

echo "====================================================="
echo "Creating Release Package..."
echo "====================================================="

# Check if binary exists
if [ ! -f "dist/RansomwareCanary" ]; then
    echo "[-] ERROR: Binary not found in dist/RansomwareCanary"
    echo "[-] Please build the binary first:"
    echo "    ./venv/bin/pyinstaller --onefile --windowed --name=\"RansomwareCanary\" --hidden-import=pystray --hidden-import=PIL main_gui.py"
    exit 1
fi

# Clean up any existing release folder
if [ -d "$RELEASE_NAME" ]; then
    echo "[*] Removing old release folder..."
    rm -rf "$RELEASE_NAME"
fi

# Create release folder
echo "[*] Creating release folder..."
mkdir -p "$RELEASE_NAME"

# Copy essential files
echo "[*] Copying files..."
cp dist/RansomwareCanary "$RELEASE_NAME/"
cp install_linux.sh "$RELEASE_NAME/"
cp README.md "$RELEASE_NAME/"
cp HOW_TO_RUN.txt "$RELEASE_NAME/"

# Make scripts executable
chmod +x "$RELEASE_NAME/RansomwareCanary"
chmod +x "$RELEASE_NAME/install_linux.sh"

# Create a simple README for the release
cat <<EOF > "$RELEASE_NAME/QUICK_START.txt"
RANSOMWARE CANARY - QUICK START
================================

1. Extract this folder
2. Open Terminal in this folder
3. Run: sudo bash install_linux.sh
4. Reboot your computer
5. Look for the system tray icon (top-right)

The app will auto-start on every boot.

For detailed instructions, see README.md
EOF

# Remove old zip if exists
if [ -f "$RELEASE_ZIP" ]; then
    echo "[*] Removing old release zip..."
    rm "$RELEASE_ZIP"
fi

# Create zip file
echo "[*] Creating zip file..."
zip -r "$RELEASE_ZIP" "$RELEASE_NAME" > /dev/null

# Get file sizes
BINARY_SIZE=$(du -h "$RELEASE_NAME/RansomwareCanary" | cut -f1)
ZIP_SIZE=$(du -h "$RELEASE_ZIP" | cut -f1)

echo ""
echo "====================================================="
echo "✅ RELEASE PACKAGE CREATED!"
echo "====================================================="
echo "Release folder: $RELEASE_NAME/"
echo "Release zip:    $RELEASE_ZIP"
echo "Binary size:    $BINARY_SIZE"
echo "Zip size:       $ZIP_SIZE"
echo ""
echo "Files included:"
ls -lh "$RELEASE_NAME" | tail -n +2
echo ""
echo "Ready for distribution! 🚀"
echo "====================================================="

