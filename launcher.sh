#!/bin/bash
# Ransomware Canary - Silent Launcher
# This script handles permissions silently and launches the app
# Used by desktop shortcuts and autostart

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Wait for desktop environment to be ready (for autostart)
if [ -n "$XDG_CURRENT_DESKTOP" ] || [ -n "$DESKTOP_SESSION" ]; then
    # Wait for display to be available
    for i in {1..30}; do
        if [ -n "$DISPLAY" ] && xset q >/dev/null 2>&1; then
            break
        fi
        sleep 0.5
    done
fi

# Grant display permission to root (silent - no output)
xhost +SI:localuser:root >/dev/null 2>&1

# Determine which method to use (binary or Python script)
BINARY_PATH="$SCRIPT_DIR/dist/RansomwareCanary"
PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
SCRIPT_PATH="$SCRIPT_DIR/main_gui.py"

if [ -f "$BINARY_PATH" ]; then
    # Use compiled binary with preserved environment, run in background
    nohup sudo -E "$BINARY_PATH" >/dev/null 2>&1 &
elif [ -f "$PYTHON_BIN" ] && [ -f "$SCRIPT_PATH" ]; then
    # Use Python script with preserved environment, run in background
    nohup sudo -E "$PYTHON_BIN" "$SCRIPT_PATH" >/dev/null 2>&1 &
else
    # Error - show notification if possible
    echo "[-] ERROR: Ransomware Canary not found!" >&2
    echo "[-] Binary: $BINARY_PATH" >&2
    echo "[-] Python: $PYTHON_BIN" >&2
    exit 1
fi

