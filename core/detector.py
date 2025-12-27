"""File system monitoring and threat detection."""

import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from core.killer import ProcessKiller
from utils.logger import ThreatLogger


class RansomwareDetector(FileSystemEventHandler):
    """Monitors file system events and triggers threat response."""
    
    def __init__(self, bait_files, logger=None, killer=None):
        """
        Initialize the detector.
        
        Args:
            bait_files: List of bait file paths to monitor
            logger: ThreatLogger instance for logging
            killer: ProcessKiller instance for termination
        """
        super().__init__()
        self.bait_files = set(os.path.abspath(f) for f in bait_files)
        self.logger = logger or ThreatLogger()
        self.killer = killer or ProcessKiller(logger=self.logger)
        self.observer = None
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        file_path = os.path.abspath(event.src_path)
        
        # Check if this is one of our bait files
        if file_path in self.bait_files:
            self._handle_threat(file_path)
    
    def on_created(self, event):
        """Handle file creation events (in case file is recreated)."""
        if event.is_directory:
            return
        
        file_path = os.path.abspath(event.src_path)
        
        # Check if this is one of our bait files
        if file_path in self.bait_files:
            self._handle_threat(file_path)
    
    def on_deleted(self, event):
        """Handle file deletion events."""
        if event.is_directory:
            return
        
        file_path = os.path.abspath(event.src_path)
        
        # Check if this is one of our bait files
        if file_path in self.bait_files:
            self._handle_threat(file_path)
    
    def on_moved(self, event):
        """Handle file move/rename events."""
        if event.is_directory:
            return
        
        file_path = os.path.abspath(event.dest_path if hasattr(event, 'dest_path') else event.src_path)
        
        # Check if this is one of our bait files
        if file_path in self.bait_files:
            self._handle_threat(file_path)
    
    def _handle_threat(self, file_path):
        """Handle a detected threat to a bait file."""
        self.logger.log_info(f"[!!!] ALERT: Bait file accessed: {file_path}")
        
        # Try to identify and kill the process
        success = self.killer.neutralize_threat(file_path)
        
        if success:
            self.logger.log_info("[✔] ACTIVE DEFENSE TRIGGERED - Threat neutralized")
        else:
            self.logger.log_error("[✗] Failed to neutralize threat - Process not identified")
    
    def start_monitoring(self, watch_directory):
        """
        Start monitoring the specified directory.
        
        Args:
            watch_directory: Directory path to monitor
        """
        watch_directory = os.path.abspath(watch_directory)
        
        self.observer = Observer()
        self.observer.schedule(self, watch_directory, recursive=False)
        self.observer.start()
        
        self.logger.log_info(f"[o] CANARY SYSTEM ACTIVE. Monitoring: {watch_directory}")
        self.logger.log_info(f"[i] Bait files: {', '.join(os.path.basename(f) for f in self.bait_files)}")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.logger.log_info("[o] Monitoring stopped")

