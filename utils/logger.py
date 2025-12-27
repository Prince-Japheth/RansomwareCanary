"""Logging utility for tracking threats and actions."""

import os
import logging
from datetime import datetime
from pathlib import Path


class ThreatLogger:
    """Handles logging of threat detection and neutralization events."""
    
    def __init__(self, log_dir="logs"):
        """Initialize logger with file and console handlers."""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create log file with timestamp
        log_file = self.log_dir / f"canary_{datetime.now().strftime('%Y%m%d')}.log"
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def log_threat_detected(self, file_path, process_name, pid):
        """Log when a threat is detected."""
        self.logger.warning(
            f"THREAT DETECTED: Process '{process_name}' (PID: {pid}) "
            f"modified bait file: {file_path}"
        )
    
    def log_threat_neutralized(self, process_name, pid):
        """Log when a threat is successfully terminated."""
        self.logger.critical(
            f"THREAT NEUTRALIZED: Process '{process_name}' (PID: {pid}) "
            f"has been terminated"
        )
    
    def log_error(self, message):
        """Log errors."""
        self.logger.error(message)
    
    def log_info(self, message):
        """Log informational messages."""
        self.logger.info(message)
    
    def log_startup(self, watch_dir, bait_files):
        """Log system startup."""
        self.logger.info("=" * 60)
        self.logger.info("RANSOMWARE CANARY SYSTEM ACTIVATED")
        self.logger.info(f"Monitoring directory: {watch_dir}")
        self.logger.info(f"Bait files: {', '.join(bait_files)}")
        self.logger.info("=" * 60)

