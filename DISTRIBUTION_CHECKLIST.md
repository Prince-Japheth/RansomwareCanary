# Distribution Checklist

Use this checklist before submitting your project to lecturers or deploying to end-users.

## ✅ Pre-Submission Checklist

### Code Files
- [x] `main_gui.py` - Cross-platform GUI version (Windows & Linux compatible)
- [x] `main.py` - Console version with all options
- [x] `install_linux.sh` - One-click Linux installer
- [x] `HOW_TO_RUN.txt` - Instructions for lecturers/users
- [x] `requirements.txt` - All dependencies listed
- [x] `README.md` - Professional documentation

### Testing Files
- [x] `ransomware_sim.py` - Ransomware simulator for testing
- [x] `test_killswitch.py` - Quick test prototype

### Core Modules
- [x] `core/detector.py` - File system monitoring
- [x] `core/killer.py` - Process identification & termination
- [x] `gui/tray.py` - System tray interface
- [x] `utils/logger.py` - Logging system
- [x] `utils/bait_gen.py` - Bait file generation

### Documentation
- [x] `README.md` - Complete project documentation
- [x] `SCREENSHOT_GUIDE.md` - Screenshot instructions for report
- [x] `HOW_TO_RUN.txt` - User instructions

## 📦 Creating Submission Package

### For Linux Lecturers

1. **Create clean ZIP file:**
   ```bash
   cd ~/Desktop
   zip -r RansomwareCanary_Submission.zip RansomwareCanary \
     -x "RansomwareCanary/venv/*" \
     -x "RansomwareCanary/__pycache__/*" \
     -x "RansomwareCanary/logs/*" \
     -x "RansomwareCanary/*.pyc" \
     -x "RansomwareCanary/.git/*"
   ```

2. **Verify ZIP contents:**
   - Should include all `.py` files
   - Should include `install_linux.sh`
   - Should include `HOW_TO_RUN.txt`
   - Should NOT include `venv/` folder
   - Should NOT include `logs/` folder

### For Windows Lecturers

**Option 1: Pre-built Executable (Best)**
1. On a Windows machine, install Python and dependencies
2. Install PyInstaller: `pip install pyinstaller`
3. Build executable:
   ```bash
   pyinstaller --onefile --windowed --name="RansomwareCanary" --hidden-import=pystray --hidden-import=PIL main_gui.py
   ```
4. Provide `dist/RansomwareCanary.exe`
5. Include `HOW_TO_RUN.txt`

**Option 2: Source Code Package**
1. Create ZIP (same as Linux, but include Windows instructions)
2. Include `HOW_TO_RUN.txt` with Windows-specific steps

## 🧪 Testing Before Submission

### Linux Testing
- [ ] Run `sudo bash install_linux.sh` - Should complete without errors
- [ ] Reboot computer - App should auto-start
- [ ] System tray icon appears (red dot)
- [ ] Left-click icon → "Start Protection" - Icon turns green
- [ ] Run `python3 ransomware_sim.py` - Should be terminated
- [ ] Check logs show "THREAT NEUTRALIZED"

### Windows Testing (If Available)
- [ ] Run `python main_gui.py` as Administrator
- [ ] System tray icon appears
- [ ] Right-click icon → "Start Protection" - Icon turns green
- [ ] Run `python ransomware_sim.py` - Should be terminated
- [ ] Check logs show "THREAT NEUTRALIZED"

### Cross-Platform Verification
- [ ] `main_gui.py` detects OS correctly (Linux vs Windows)
- [ ] Directory detection works on both platforms
- [ ] No Linux-specific code breaks on Windows
- [ ] No Windows-specific code breaks on Linux

## 📋 Files to Include in Submission

### Required Files
```
RansomwareCanary/
├── main.py
├── main_gui.py
├── install_linux.sh
├── HOW_TO_RUN.txt
├── requirements.txt
├── README.md
├── ransomware_sim.py
├── test_killswitch.py
├── core/
│   ├── __init__.py
│   ├── detector.py
│   └── killer.py
├── gui/
│   ├── __init__.py
│   └── tray.py
└── utils/
    ├── __init__.py
    ├── logger.py
    └── bait_gen.py
```

### Optional Files (For Report)
- `SCREENSHOT_GUIDE.md` - For your reference
- `DISTRIBUTION_CHECKLIST.md` - This file

### Files to EXCLUDE
- `venv/` - Virtual environment (too large)
- `__pycache__/` - Python cache files
- `logs/` - Log files (personal data)
- `*.pyc` - Compiled Python files
- `.git/` - Git repository (if present)

## 🎯 Final Verification

Before submitting, verify:

1. **Code Quality:**
   - [ ] No syntax errors
   - [ ] All imports work
   - [ ] Cross-platform compatibility verified

2. **Documentation:**
   - [ ] README.md is complete and professional
   - [ ] HOW_TO_RUN.txt has clear instructions
   - [ ] All code comments are clear

3. **Functionality:**
   - [ ] Canary detects and kills simulator
   - [ ] System tray icon works
   - [ ] Auto-start works (Linux)
   - [ ] Logging works correctly

4. **Distribution:**
   - [ ] ZIP file created successfully
   - [ ] ZIP file size is reasonable (< 5MB without venv)
   - [ ] All necessary files included
   - [ ] No unnecessary files included

## 📝 Submission Notes

**For Lecturers:**
- Include a brief cover letter explaining the project
- Mention it's a "Zero-Infrastructure Endpoint Protection Agent"
- Highlight the cross-platform support
- Note that Linux version includes one-click installer

**For Windows Users:**
- If you can't build the .exe, provide clear source code instructions
- Emphasize running as Administrator
- Include troubleshooting section

**For Linux Users:**
- Emphasize the `install_linux.sh` script for easy setup
- Mention auto-start capability
- Note the left-click vs right-click difference

---

**Good luck with your submission! 🚀**

