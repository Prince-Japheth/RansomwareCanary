#!/usr/bin/env python3
"""
Quick test script to verify the kill-switch functionality.

This creates a bait file and monitors it. Try to modify the file
and see if the process gets killed.
"""

import sys
import time
import os
import psutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# CONFIGURATION
BAIT_FILENAME = "_BAIT_FILE.txt"
WATCH_DIR = os.path.dirname(os.path.abspath(__file__))
BAIT_PATH = os.path.join(WATCH_DIR, BAIT_FILENAME)


class RansomwareKiller(FileSystemEventHandler):
    def on_modified(self, event):
        # We only care if the bait file was touched
        if event.src_path == BAIT_PATH:
            print(f"[!!!] ALERT: Bait file modified!")
            self.terminate_process()

    def terminate_process(self):
        print("[*] ACTIVE DEFENSE TRIGGERED")
        
        # Scan for any process holding the bait file open
        for proc in psutil.process_iter(['pid', 'name', 'open_files']):
            try:
                if proc.info['open_files']:
                    for file in proc.info['open_files']:
                        if file.path == BAIT_PATH:
                            print(f"[XXX] DETECTED MALWARE: {proc.info['name']} (PID: {proc.info['pid']})")
                            print(f"[XXX] KILLING PROCESS...")
                            proc.kill()  # THE KILL SHOT
                            print(f"[✔] THREAT NEUTRALIZED.")
                            return
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue


def setup_bait():
    """Creates the trap file if it doesn't exist."""
    if not os.path.exists(BAIT_PATH):
        with open(BAIT_PATH, "w") as f:
            f.write("Do not touch this file. It is a trap.")
        print(f"[+] Bait file created at: {BAIT_PATH}")


def start_monitoring():
    setup_bait()
    event_handler = RansomwareKiller()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"[o] CANARY SYSTEM ACTIVE. Monitoring: {WATCH_DIR}")
    print(f"[i] Try to open '{BAIT_FILENAME}' and save it. See what happens.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    # Check for Admin/Root (Required to kill processes)
    if os.name == 'nt':  # Windows
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    else:  # Linux/Mac
        is_admin = os.geteuid() == 0
    
    if not is_admin:
        print("[-] WARNING: You are not running as Root/Admin.")
        print("[-] You might not have permission to kill the malware process.")
        print("[-] Please run this script with 'sudo' or 'Run as Administrator'.")
        # We don't exit, we let you try, but it might fail.
    
    start_monitoring()

