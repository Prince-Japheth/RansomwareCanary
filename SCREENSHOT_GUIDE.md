# Screenshot Guide for Project Report

This document lists all the screenshots you should capture for your project report and where to place them in your document.

## 📸 Required Screenshots

### **Chapter 1: Introduction**

#### Screenshot 1.1: System Tray Icon (Stopped State)
- **What to capture:** System tray area showing the red dot icon
- **How to get it:**
  1. Run `sudo python3 main_gui.py`
  2. Wait for icon to appear (red dot = stopped)
  3. Take screenshot of the system tray area (top-right corner)
- **Caption:** "System Tray Icon - Stopped State (Red Dot)"
- **Where:** Chapter 1, Section 1.1 (Background) or Chapter 3 (System Design)

---

#### Screenshot 1.2: System Tray Menu
- **What to capture:** Left-click menu showing "Start Protection", "Stop Protection", "Exit"
- **How to get it:**
  1. Left-click the system tray icon
  2. Capture the dropdown menu
- **Caption:** "System Tray Menu Interface"
- **Where:** Chapter 3, Section 3.1 (System Architecture)

---

### **Chapter 3: System Design & Technical Implementation**

#### Screenshot 3.1: Terminal Output - System Startup
- **What to capture:** Terminal showing the startup messages
- **How to get it:**
  1. Run `sudo python3 main_gui.py`
  2. Capture the terminal output showing:
     - "🛡️ RANSOMWARE CANARY - GUI MODE"
     - "Target Directory: /home/japheth/Desktop/RansomwareCanary"
     - "Left-Click the System Tray Icon..."
- **Caption:** "System Initialization - Correct Directory Detection"
- **Where:** Chapter 3, Section 3.5 (Handling Privileged Execution)

---

#### Screenshot 3.2: System Tray Icon (Active State)
- **What to capture:** System tray showing the green dot icon
- **How to get it:**
  1. Left-click icon → "Start Protection"
  2. Icon should turn green
  3. Capture the green dot icon
- **Caption:** "System Tray Icon - Active Protection State (Green Dot)"
- **Where:** Chapter 3, Section 3.1 (System Architecture)

---

#### Screenshot 3.3: Project Directory Structure
- **What to capture:** File manager or terminal showing the project structure
- **How to get it:**
  1. Open file manager in `/home/japheth/Desktop/RansomwareCanary`
  2. Or run: `tree -L 2` or `ls -R`
  3. Capture the directory structure
- **Caption:** "Project Directory Structure"
- **Where:** Chapter 3, Section 3.1 (System Architecture)

---

#### Screenshot 3.4: Code Snippet - Detector Module
- **What to capture:** Your IDE/editor showing `core/detector.py` (key parts)
- **How to get it:**
  1. Open `core/detector.py` in your editor
  2. Highlight the `on_modified()` method and `_handle_threat()` method
  3. Take screenshot
- **Caption:** "File System Event Handler - Detector Module"
- **Where:** Chapter 4, Section 4.1 (Implementation - Detector)

---

#### Screenshot 3.5: Code Snippet - Killer Module
- **What to capture:** Your IDE/editor showing `core/killer.py` (key parts)
- **How to get it:**
  1. Open `core/killer.py` in your editor
  2. Highlight the `find_process_by_file()` method and `kill_process()` method
  3. Take screenshot
- **Caption:** "Process Identification and Termination - Killer Module"
- **Where:** Chapter 4, Section 4.2 (Implementation - Killer)

---

### **Chapter 5: Testing & Results**

#### Screenshot 5.1: Ransomware Simulator Running
- **What to capture:** Terminal running `python3 ransomware_sim.py`
- **How to get it:**
  1. Open a new terminal (Terminal 2)
  2. Run `python3 ransomware_sim.py`
  3. Capture the output showing:
     - `[☠️] MALWARE STARTED. Targeting: _BAIT_FILE.txt`
     - `[☠️] File modified. Waiting for encryption...`
     - `[☠️] Encrypting chunk 1...`
- **Caption:** "Ransomware Simulator - Attack in Progress"
- **Where:** Chapter 5, Section 5.1 (Test Scenario)

---

#### Screenshot 5.2: Canary Detection Logs
- **What to capture:** Canary terminal showing threat detection
- **How to get it:**
  1. In Terminal 1 (where Canary is running)
  2. Capture the output showing:
     - `[!!!] ALERT: Bait file accessed: ...`
     - `[XXX] DETECTED MALWARE: python3 (PID: xxxxx)`
     - `[XXX] KILLING PROCESS...`
     - `[✔] THREAT NEUTRALIZED.`
- **Caption:** "Real-Time Threat Detection and Neutralization"
- **Where:** Chapter 5, Section 5.2 (Results)

---

#### Screenshot 5.3: Simulator Terminated
- **What to capture:** Simulator terminal showing "Terminated" message
- **How to get it:**
  1. In Terminal 2 (simulator terminal)
  2. After Canary kills it, capture the terminal showing:
     - `Terminated` (or `Killed`)
     - The process should stop mid-execution
- **Caption:** "Ransomware Process Terminated - Active Defense Successful"
- **Where:** Chapter 5, Section 5.2 (Results) - **THIS IS YOUR PROOF!**

---

#### Screenshot 5.4: Side-by-Side Comparison
- **What to capture:** Both terminals side-by-side
- **How to get it:**
  1. Arrange Terminal 1 (Canary) and Terminal 2 (Simulator) side-by-side
  2. Run the simulator
  3. Capture both terminals showing:
     - Left: Canary detecting and killing
     - Right: Simulator being terminated
- **Caption:** "Real-Time Attack Detection and Response - Side-by-Side View"
- **Where:** Chapter 5, Section 5.2 (Results) - **MAIN PROOF SHOT**

---

#### Screenshot 5.5: Log File Contents
- **What to capture:** Log file showing the incident
- **How to get it:**
  1. Open `logs/canary_YYYYMMDD.log`
  2. Show the log entry with:
     - Timestamp
     - "THREAT DETECTED"
     - "THREAT NEUTRALIZED"
     - Process name and PID
- **Caption:** "Forensic Log Entry - Threat Incident Record"
- **Where:** Chapter 5, Section 5.2 (Results) or Chapter 3, Section 3.4

---

#### Screenshot 5.6: System Tray Icon After Attack
- **What to capture:** System tray icon (should still be green, showing active)
- **How to get it:**
  1. After the attack is neutralized
  2. Capture the system tray showing green icon
  3. Optionally hover to show tooltip "Ransomware Canary: ACTIVE"
- **Caption:** "System Status After Threat Neutralization"
- **Where:** Chapter 5, Section 5.2 (Results)

---

### **Chapter 6: Conclusion**

#### Screenshot 6.1: System Resource Usage
- **What to capture:** System monitor showing low CPU/memory usage
- **How to get it:**
  1. Run `htop` or `top` while Canary is running
  2. Find the Python process running the Canary
  3. Show low CPU usage (< 1%) and minimal memory
- **Caption:** "System Resource Usage - Zero-Overhead Monitoring"
- **Where:** Chapter 6, Section 6.2 (Future Improvements) or Chapter 3, Section 3.2

---

## 📋 Screenshot Checklist

Before submitting your report, verify you have:

- [ ] System tray icon (red/stopped state)
- [ ] System tray icon (green/active state)
- [ ] System tray menu
- [ ] Terminal startup output
- [ ] Project directory structure
- [ ] Code snippet - Detector module
- [ ] Code snippet - Killer module
- [ ] Ransomware simulator running
- [ ] Canary detection logs
- [ ] **Simulator terminated message (CRITICAL)**
- [ ] Side-by-side comparison (BEST PROOF)
- [ ] Log file contents
- [ ] System resource usage

## 🎯 Priority Screenshots (Must Have)

These are the most important screenshots that prove your system works:

1. **Screenshot 5.4: Side-by-Side Comparison** - Shows the attack and defense in real-time
2. **Screenshot 5.3: Simulator Terminated** - Shows the word "Terminated" (your proof)
3. **Screenshot 5.2: Canary Detection Logs** - Shows the technical details
4. **Screenshot 3.2: Green Icon** - Shows the GUI working
5. **Screenshot 3.1: Startup Output** - Shows correct directory detection

## 💡 Tips for Taking Screenshots

1. **Use a clean desktop** - Close unnecessary windows
2. **Use consistent terminal theme** - Makes it look professional
3. **Add annotations** - Use arrows or boxes to highlight important parts
4. **Use high resolution** - At least 1920x1080
5. **Name files clearly** - e.g., `screenshot_5_4_side_by_side.png`
6. **Add timestamps** - Some screenshot tools can add timestamps automatically

## 📐 Screenshot Dimensions

- **Full screen:** 1920x1080 or higher
- **Terminal only:** 800x600 minimum
- **System tray:** 200x100 (zoomed/cropped)
- **Code snippets:** 1000x400 (showing 20-30 lines)

---

**Good luck with your report! These screenshots will make your project stand out.**

