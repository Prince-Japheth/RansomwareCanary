"""Process identification and termination module."""

import os
import time
import psutil
from typing import Optional, Tuple


class ProcessKiller:
    """Handles identification and termination of malicious processes."""
    
    def __init__(self, logger=None):
        """Initialize the process killer."""
        self.logger = logger
    
    def find_process_by_file(self, file_path: str) -> Optional[Tuple[psutil.Process, str]]:
        """
        Find the process that has the specified file open.
        
        This is the "secret sauce" - finding the exact PID that modified a file.
        We scan all processes and check their open file handles.
        
        Args:
            file_path: Path to the file we're looking for
        
        Returns:
            Tuple of (process, process_name) if found, None otherwise
        """
        file_path = os.path.abspath(file_path)
        file_path_normalized = os.path.normpath(file_path)
        
        # Give a small delay to ensure the process has the file open
        # For ransomware that holds files open, this should be enough
        time.sleep(0.1)
        
        # Scan multiple times to catch processes that just opened the file
        for scan_attempt in range(3):
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    # Use proc.open_files() method - more reliable
                    try:
                        open_files = proc.open_files()
                        for file_info in open_files:
                            proc_file_path = os.path.normpath(os.path.abspath(file_info.path))
                            if proc_file_path == file_path_normalized:
                                return (proc, proc.info['name'])
                    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                        continue
                    
                    # Also check the info dict if available
                    try:
                        if hasattr(proc, 'info') and proc.info.get('open_files'):
                            for file_info in proc.info['open_files']:
                                if hasattr(file_info, 'path'):
                                    proc_file_path = os.path.normpath(os.path.abspath(file_info.path))
                                    if proc_file_path == file_path_normalized:
                                        return (proc, proc.info['name'])
                    except:
                        continue
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            # Small delay between scans
            if scan_attempt < 2:
                time.sleep(0.05)
        
        return None
    
    def find_recent_process(self, file_path: str, time_window: float = 2.0) -> Optional[Tuple[psutil.Process, str]]:
        """
        Find the most recently active process that might have modified the file.
        
        This is a fallback method when we can't find the file handle directly.
        We look for processes that have been active recently.
        
        Args:
            file_path: Path to the modified file
            time_window: Time window in seconds to look for recent activity
        
        Returns:
            Tuple of (process, process_name) if found, None otherwise
        """
        current_time = time.time()
        
        # First, try to find by open file handle
        result = self.find_process_by_file(file_path)
        if result:
            return result
        
        # Fallback: Find processes that have been active recently
        # This is less precise but can catch processes that closed the file quickly
        candidates = []
        
        for proc in psutil.process_iter(['pid', 'name', 'create_time']):
            try:
                # Check if process was created or had activity in the time window
                proc_create_time = proc.info.get('create_time', 0)
                if proc_create_time and (current_time - proc_create_time) < time_window:
                    # Check if this process might be related to file operations
                    proc_name = proc.info['name'].lower()
                    # Common file editor/ransomware process names
                    suspicious_keywords = ['notepad', 'gedit', 'nano', 'vim', 'code', 
                                         'explorer', 'thunderbird', 'outlook', 'winword']
                    if any(keyword in proc_name for keyword in suspicious_keywords):
                        candidates.append((proc, proc.info['name']))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Return the most recently created process if any candidates found
        if candidates:
            # Sort by creation time (most recent first)
            candidates.sort(key=lambda x: x[0].create_time(), reverse=True)
            return candidates[0]
        
        return None
    
    def kill_process(self, process: psutil.Process, process_name: str) -> bool:
        """
        Terminate a process immediately.
        
        Args:
            process: The psutil.Process object to kill
            process_name: Name of the process for logging
        
        Returns:
            True if successful, False otherwise
        """
        try:
            pid = process.pid
            
            if self.logger:
                self.logger.log_threat_neutralized(process_name, pid)
            
            # Try graceful termination first
            try:
                process.terminate()
                # Wait up to 2 seconds for graceful shutdown
                process.wait(timeout=2)
            except psutil.TimeoutExpired:
                # Force kill if graceful termination failed
                process.kill()
                process.wait(timeout=1)
            
            return True
            
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            if self.logger:
                self.logger.log_error(f"Failed to kill process {process_name}: {e}")
            return False
    
    def neutralize_threat(self, file_path: str) -> bool:
        """
        Main method to find and kill the process that modified the bait file.
        
        Args:
            file_path: Path to the bait file that was modified
        
        Returns:
            True if threat was neutralized, False otherwise
        """
        # Try to find the process by open file handle
        result = self.find_process_by_file(file_path)
        
        if not result:
            # Fallback to recent process detection
            result = self.find_recent_process(file_path)
        
        if result:
            process, process_name = result
            return self.kill_process(process, process_name)
        else:
            if self.logger:
                self.logger.log_error(
                    f"Could not identify process that modified {file_path}"
                )
            return False

