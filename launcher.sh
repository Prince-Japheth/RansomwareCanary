#!/bin/bash
# Ransomware Canary - Silent Launcher
# This script handles permissions silently and launches the app
# Used by desktop shortcuts and autostart

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Grant display permission to root (silent - no output)
xhost +SI:localuser:root >/dev/null 2>&1

# Determine which method to use (binary or Python script)
BINARY_PATH="$SCRIPT_DIR/dist/RansomwareCanary"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
SCRIPT_PATH="$SCRIPT_DIR/main_gui.py"

if [ -f "$BINARY_PATH" ]; then
    # Use compiled binary with preserved environment
    sudo -E "$BINARY_PATH"
elif [ -f "$PYTHON_BIN" ] && [ -f "$SCRIPT_PATH" ]; then
    # Use Python script with preserved environment
    sudo -E "$PYTHON_BIN" "$SCRIPT_PATH"
else
    # Error - show notification if possible
    echo "[-] ERROR: Ransomware Canary not found!"
    echo "[-] Binary: $BINARY_PATH"
    echo "[-] Python: $PYTHON_BIN"
    exit 1
fi

