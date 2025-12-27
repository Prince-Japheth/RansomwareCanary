#!/usr/bin/env python3
"""
Ransomware Canary - Zero-Infrastructure Endpoint Protection Agent

This system monitors bait files and immediately terminates any process
that attempts to modify them, providing active defense against ransomware.
"""

import os
import sys
import time
import threading
import argparse
from pathlib import Path

from core.detector import RansomwareDetector
from core.killer import ProcessKiller
from utils.logger import ThreatLogger
from utils.bait_gen import create_bait_file, create_all_bait_files
from gui.tray import TrayIcon, SimpleTkinterGUI


def check_permissions():
    """Check if running with sufficient permissions."""
    if os.name == 'nt':  # Windows
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            is_admin = False
    else:  # Linux/Mac
        is_admin = os.geteuid() == 0
    
    return is_admin


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Ransomware Canary - Active Endpoint Protection"
    )
    parser.add_argument(
        '--watch-dir',
        type=str,
        default=os.getcwd(),
        help='Directory to monitor (default: current directory)'
    )
    parser.add_argument(
        '--bait-file',
        type=str,
        default=None,
        help='Specific bait file to create (default: _backup_codes.txt)'
    )
    parser.add_argument(
        '--all-bait',
        action='store_true',
        help='Create all standard bait files'
    )
    parser.add_argument(
        '--no-gui',
        action='store_true',
        help='Run without GUI (console mode only)'
    )
    
    args = parser.parse_args()
    
    # Check permissions
    is_admin = check_permissions()
    if not is_admin:
        print("=" * 60)
        print("⚠️  WARNING: Not running as Root/Administrator")
        print("⚠️  You may not have permission to kill processes")
        print("⚠️  On Linux, run with: sudo python3 main.py")
        print("⚠️  On Windows, run as Administrator")
        print("=" * 60)
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Setup
    watch_dir = os.path.abspath(args.watch_dir)
    logger = ThreatLogger()
    
    # Create bait files
    if args.all_bait:
        bait_files = create_all_bait_files(watch_dir)
        logger.log_info(f"Created {len(bait_files)} bait files")
    else:
        bait_file = create_bait_file(watch_dir, args.bait_file)
        bait_files = [bait_file]
        logger.log_info(f"Created bait file: {bait_file}")
    
    # Initialize components
    killer = ProcessKiller(logger=logger)
    detector = RansomwareDetector(bait_files, logger=logger, killer=killer)
    
    # Log startup
    logger.log_startup(watch_dir, [os.path.basename(f) for f in bait_files])
    
    # Start monitoring
    detector.start_monitoring(watch_dir)
    
    # Setup GUI
    gui = None
    if not args.no_gui:
        try:
            gui = TrayIcon(detector, logger=logger)
            gui.run()
        except Exception as e:
            logger.log_error(f"Failed to start tray icon: {e}")
            try:
                # Fallback to tkinter
                gui = SimpleTkinterGUI(detector, logger=logger)
                gui_thread = threading.Thread(target=gui.run, daemon=True)
                gui_thread.start()
            except Exception as e2:
                logger.log_error(f"Failed to start GUI: {e2}")
                logger.log_info("Running in console mode")
    
    # Main loop
    try:
        print("\n" + "=" * 60)
        print("🛡️  RANSOMWARE CANARY ACTIVE")
        print("=" * 60)
        print(f"Monitoring: {watch_dir}")
        print(f"Bait files: {', '.join(os.path.basename(f) for f in bait_files)}")
        print("\n💡 Try opening and modifying a bait file to test the system!")
        print("Press Ctrl+C to stop\n")
        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n[!] Shutting down...")
        detector.stop_monitoring()
        logger.log_info("Ransomware Canary stopped")
        sys.exit(0)


if __name__ == "__main__":
    main()

