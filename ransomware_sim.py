#!/usr/bin/env python3
"""
Ransomware Simulator - For Testing the Canary System

This script simulates ransomware behavior by opening a bait file,
modifying it, and holding it open for an extended period (simulating
encryption time). This allows the Canary system to detect and kill it.

WARNING: This is for testing purposes only!
"""

import time
import os
import sys

# The target file (must match your Canary's bait)
TARGET = "_BAIT_FILE.txt"


def attack():
    """Simulate a ransomware attack on the bait file."""
    if not os.path.exists(TARGET):
        print(f"[-] Target {TARGET} not found!")
        print(f"[i] Make sure the Canary is running and has created the bait file.")
        return

    print(f"[X] MALWARE STARTED. Targeting: {TARGET}")
    print(f"[X] Opening file and holding it...")
    
    try:
        # We open the file and KEEP IT OPEN to simulate encryption time
        with open(TARGET, "a") as f:
            f.write("\nMALWARE_WAS_HERE")
            f.flush()  # Force write to disk to trigger the Canary
            
            print("[X] File modified. Waiting for encryption (simulating 10s)...")
            # This sleep forces the process to hold the file handle open
            # This gives your Canary time to find and kill us.
            for i in range(10):
                time.sleep(1)
                print(f"[X] Encrypting chunk {i+1}...")
                
        print("[-] ATTACK SUCCESSFUL. (If you see this, the Canary FAILED).")
        
    except Exception as e:
        print(f"[-] Attack failed: {e}")


if __name__ == "__main__":
    attack()

