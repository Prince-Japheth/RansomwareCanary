"""Bait file generation utility."""

import os
from pathlib import Path


# Common bait filenames that ransomware typically targets
BAIT_FILENAMES = [
    "_backup_codes.txt",
    "_BAIT_FILE.txt",
    "backup_keys.txt",
    "wallet_backup.dat",
    "recovery_codes.txt",
    "master_key.txt"
]


def create_bait_file(directory, filename=None):
    """
    Create a bait file in the specified directory.
    
    Args:
        directory: Path to directory where bait file should be created
        filename: Optional specific filename. If None, uses first from BAIT_FILENAMES
    
    Returns:
        Path to created bait file
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    
    if filename is None:
        filename = BAIT_FILENAMES[0]
    
    bait_path = directory / filename
    
    # Create bait file with content that looks valuable
    if not bait_path.exists():
        content = """WARNING: This file is a honeypot trap.
        
Do not modify this file. Any process that attempts to modify this file
will be immediately terminated by the Ransomware Canary protection system.

This file is monitored 24/7 for unauthorized access.
"""
        with open(bait_path, 'w') as f:
            f.write(content)
    
    return str(bait_path)


def create_all_bait_files(directory):
    """
    Create all standard bait files in the directory.
    
    Args:
        directory: Path to directory where bait files should be created
    
    Returns:
        List of paths to created bait files
    """
    directory = Path(directory)
    bait_files = []
    
    for filename in BAIT_FILENAMES:
        bait_path = create_bait_file(directory, filename)
        bait_files.append(bait_path)
    
    return bait_files

