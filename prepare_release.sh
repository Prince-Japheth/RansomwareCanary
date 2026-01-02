#!/bin/bash
# Ransomware Canary - GitHub Release Preparation Script
# This creates release packages for both Linux and Windows

VERSION="${1:-v1.0.0}"
RELEASE_DIR="release_${VERSION}"

echo "====================================================="
echo "Preparing GitHub Release: $VERSION"
echo "====================================================="
echo ""

# Clean up old release directory
if [ -d "$RELEASE_DIR" ]; then
    echo "[*] Removing old release directory..."
    rm -rf "$RELEASE_DIR"
fi

mkdir -p "$RELEASE_DIR"

# Check for binaries
if [ ! -f "dist/RansomwareCanary" ]; then
    echo "[-] ERROR: Linux binary not found!"
    echo "[-] Build it first: ./venv/bin/pyinstaller --onefile --windowed --name=\"RansomwareCanary\" --hidden-import=pystray --hidden-import=PIL --add-data \"icons:icons\" main_gui.py"
    exit 1
fi

if [ ! -f "dist/RansomwareCanary.exe" ]; then
    echo "[-] WARNING: Windows binary not found!"
    echo "[-] Build it on Windows or with Wine"
fi

echo "[*] Creating Linux release package..."

# Linux Release
LINUX_DIR="$RELEASE_DIR/RansomwareCanary_Linux_${VERSION}"
mkdir -p "$LINUX_DIR"

cp dist/RansomwareCanary "$LINUX_DIR/"
cp install_linux.sh "$LINUX_DIR/"
cp uninstall_linux.sh "$LINUX_DIR/"
cp launcher.sh "$LINUX_DIR/"
cp README.md "$LINUX_DIR/"
cp HOW_TO_RUN.txt "$LINUX_DIR/"

chmod +x "$LINUX_DIR/RansomwareCanary"
chmod +x "$LINUX_DIR/install_linux.sh"
chmod +x "$LINUX_DIR/uninstall_linux.sh"
chmod +x "$LINUX_DIR/launcher.sh"

# Create Linux zip
cd "$RELEASE_DIR"
zip -r "RansomwareCanary_Linux_${VERSION}.zip" "RansomwareCanary_Linux_${VERSION}" > /dev/null
cd ..

# Windows Release (if available)
if [ -f "dist/RansomwareCanary.exe" ]; then
    echo "[*] Creating Windows release package..."
    
    WINDOWS_DIR="$RELEASE_DIR/RansomwareCanary_Windows_${VERSION}"
    mkdir -p "$WINDOWS_DIR"
    
    cp dist/RansomwareCanary.exe "$WINDOWS_DIR/"
    cp install_windows.bat "$WINDOWS_DIR/"
    cp README.md "$WINDOWS_DIR/"
    cp HOW_TO_RUN.txt "$WINDOWS_DIR/"
    
    # Create Windows zip
    cd "$RELEASE_DIR"
    zip -r "RansomwareCanary_Windows_${VERSION}.zip" "RansomwareCanary_Windows_${VERSION}" > /dev/null
    cd ..
fi

# Source code package
echo "[*] Creating source code package..."
cd ..
zip -r "RansomwareCanary/release_${VERSION}/RansomwareCanary_Source_${VERSION}.zip" RansomwareCanary \
  -x "RansomwareCanary/venv/*" \
  -x "RansomwareCanary/__pycache__/*" \
  -x "RansomwareCanary/logs/*" \
  -x "RansomwareCanary/dist/*" \
  -x "RansomwareCanary/build/*" \
  -x "RansomwareCanary/*.pyc" \
  -x "RansomwareCanary/*.spec" \
  -x "RansomwareCanary/release_*/*" \
  -x "RansomwareCanary/.git/*" > /dev/null
cd RansomwareCanary

echo ""
echo "====================================================="
echo "✅ Release packages created in: $RELEASE_DIR/"
echo "====================================================="
echo ""
echo "Files ready for GitHub Release:"
ls -lh "$RELEASE_DIR"/*.zip 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/Prince-Japheth/RansomwareCanary/releases/new"
echo "2. Tag: $VERSION"
echo "3. Title: Release $VERSION"
echo "4. Upload the .zip files from $RELEASE_DIR/"
echo "5. Copy release notes from RELEASE_NOTES_TEMPLATE.md"
echo "====================================================="

