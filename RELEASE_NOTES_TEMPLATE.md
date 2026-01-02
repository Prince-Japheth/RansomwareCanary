# Release Notes - v1.0.1

## What's New in v1.0.1

### Bug Fixes
- **Fixed auto-start on boot**: App now properly starts automatically after reboot
  - Launcher waits for desktop environment to be ready
  - Runs in background without blocking
  - Properly handles display permissions
- **Fixed icon rendering**: SVG icons now render correctly
  - No black background (transparency preserved)
  - Proper sizing without overflow
  - Clean shield icons (ShieldTick for active, ShieldCross for stopped)

### Improvements
- Auto-start protection on launch (no manual "Start" needed)
- Professional SVG icons with transparency support
- All emojis removed from codebase for enterprise compatibility
- Improved launcher script reliability

## Downloads

### Linux
- **RansomwareCanary_Linux_v1.0.1.zip** - Pre-built binary + installer
  - Extract and run: `sudo bash install_linux.sh`
  - No Python required!
  - Auto-starts on boot

### Windows  
- **RansomwareCanary_Windows_v1.0.1.zip** - Pre-built executable + installer
  - Extract and run: `install_windows.bat` (as Administrator)
  - Adds to Start Menu and auto-starts on boot

### Source Code
- **RansomwareCanary_Source_v1.0.1.zip** - Full source code
  - For developers or users who want to build from source
  - Requires Python 3.8+ and dependencies from `requirements.txt`

## Installation

### Linux
1. Download `RansomwareCanary_Linux_v1.0.1.zip`
2. Extract the folder
3. Open Terminal in the extracted folder
4. Run: `sudo bash install_linux.sh`
5. Reboot your computer
6. App will auto-start - look for shield icon in system tray

### Windows
1. Download `RansomwareCanary_Windows_v1.0.1.zip`
2. Extract the folder
3. Right-click `install_windows.bat` → Run as Administrator
4. App will appear in Start Menu and auto-start on boot
5. Look for shield icon in system tray

## Testing

Use the included `ransomware_sim.py` to test the system:
```bash
python3 ransomware_sim.py  # Linux
python ransomware_sim.py   # Windows
```

The simulator should be terminated immediately by the Canary.

## Documentation

See `README.md` and `HOW_TO_RUN.txt` for detailed instructions.

## Requirements

- **Linux**: Ubuntu/Debian-based distro, sudo access
- **Windows**: Windows 10/11, Administrator access
- **No Python required** for pre-built binaries!

## Known Issues

None at this time.

## Credits

Built for educational purposes as a Practical Skill Assessment (PSA) project.

