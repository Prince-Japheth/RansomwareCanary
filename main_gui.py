#!/usr/bin/env python3
"""
Ransomware Canary - GUI Version with System Tray

This version provides a system tray interface with start/stop controls.
Cross-platform: Works on Linux, Windows, and macOS
Run with: sudo python3 main_gui.py (Linux) or as Administrator (Windows)
"""

import os
import sys
import threading
import logging
import platform
import time
from pathlib import Path

from core.detector import RansomwareDetector
from core.killer import ProcessKiller
from utils.logger import ThreatLogger
from utils.bait_gen import create_bait_file
from gui.tray import SystemTrayApp

# SETUP LOGGING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)


def get_target_directory():
    """Universal Desktop Finder (Windows & Linux Sudo-Safe)"""
    system_os = platform.system()
    
    if system_os == "Linux" and os.geteuid() == 0:
        # Linux Root Mode: Try to find the real user
        sudo_user = os.environ.get('SUDO_USER')
        if sudo_user:
            return os.path.join('/home', sudo_user, 'Desktop', 'RansomwareCanary')
            
    # Windows / Standard Linux User / Fallback
    # On Windows, os.path.expanduser("~") correctly finds the user profile
    return os.path.join(os.path.expanduser("~"), "Desktop", "RansomwareCanary")


# GLOBAL CONFIG
WATCH_DIR = get_target_directory()
BAIT_FILE = "_BAIT_FILE.txt"

# GLOBAL STATE
detector = None
logger = None
killer = None


def start_monitoring():
    """Start the monitoring service."""
    global detector, logger, killer
    
    logging.info("============================================================")
    logging.info("RANSOMWARE CANARY SYSTEM ACTIVATED")
    logging.info(f"OS: {platform.system()} {platform.release()}")
    logging.info(f"Monitoring directory: {WATCH_DIR}")
    logging.info(f"Bait files: {BAIT_FILE}")
    logging.info("============================================================")
    
    # Ensure directory exists
    if not os.path.exists(WATCH_DIR):
        try:
            os.makedirs(WATCH_DIR, exist_ok=True)
        except Exception as e:
            logging.error(f"Cannot create directory {WATCH_DIR}: {e}")
            return
    
    # Initialize logger if not already done
    if logger is None:
        logger = ThreatLogger()
    
    # Create the bait file
    bait_path = os.path.join(WATCH_DIR, BAIT_FILE)
    if not os.path.exists(bait_path):
        try:
            bait_path = create_bait_file(WATCH_DIR, BAIT_FILE)
            logger.log_info(f"Created bait file: {bait_path}")
        except Exception as e:
            logging.warning(f"Bait file setup warning: {e}")
            return
    else:
        bait_path = os.path.abspath(bait_path)
    
    # Fix permissions so regular users can trigger it (for testing)
    # Linux Permissions Fix (Only needed on Linux)
    if platform.system() == "Linux":
        try:
            os.chmod(bait_path, 0o666)
        except Exception as e:
            logging.warning(f"Could not set permissions on bait file: {e}")
    
    # Initialize components
    if killer is None:
        killer = ProcessKiller(logger=logger)
    
    bait_files = [bait_path]
    detector = RansomwareDetector(bait_files, logger=logger, killer=killer)
    
    # Log startup
    logger.log_startup(WATCH_DIR, [os.path.basename(f) for f in bait_files])
    
    # Start monitoring
    detector.start_monitoring(WATCH_DIR)
    logging.info(f"[o] CANARY SYSTEM ACTIVE. Monitoring: {WATCH_DIR}")


def stop_monitoring():
    """Stop the monitoring service."""
    global detector, logger
    
    if detector:
        logging.info("Stopping Monitoring Service...")
        detector.stop_monitoring()
        detector = None
        if logger:
            logger.log_info("[-] Service Stopped.")


if __name__ == "__main__":
    # Check privileges only for Linux
    if platform.system() == "Linux" and os.geteuid() != 0:
        print("=" * 60)
        print("[-] LINUX WARNING: You should run this with 'sudo' to kill processes.")
        print("[-] Try: sudo python3 main_gui.py")
        print("[-] Continuing anyway, but process termination may fail...")
        print("=" * 60)
        # We don't exit, we let them run it to test the GUI, but the kill might fail.
    
    print(f"\n[i] Target Directory: {WATCH_DIR}")
    print("[i] Check your System Tray (Top Right or Bottom Right) for the Shield Icon.")
    print("[i] Left-Click (Ubuntu) or Right-Click (Windows) the icon to Start/Stop protection\n")
    
    # Launch GUI
    app = SystemTrayApp(start_callback=start_monitoring, stop_callback=stop_monitoring)
    app.run()
