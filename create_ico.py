#!/usr/bin/env python3
"""Create Windows .ico file from PNG icon."""

from PIL import Image
import os

def create_ico():
    """Create a Windows .ico file from the green shield icon."""
    png_path = "icons/shield_green.png"
    
    if not os.path.exists(png_path):
        print(f"[-] ERROR: {png_path} not found!")
        return
    
    # Open the PNG
    img = Image.open(png_path)
    
    # Create ICO with multiple sizes (Windows standard)
    ico_path = "icons/shield.ico"
    img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])
    print(f"[+] Created: {ico_path}")

if __name__ == "__main__":
    create_ico()

