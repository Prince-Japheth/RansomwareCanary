#!/usr/bin/env python3
"""Create shield icon files for the application."""

from PIL import Image, ImageDraw
import os

def create_shield_icon(color, filename):
    """Create a shield icon and save it as PNG."""
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
    dc = ImageDraw.Draw(image)
    
    # Define shield color
    if color == "green":
        fill_color = (0, 200, 0)  # Green = Active/Protected
        outline_color = (0, 150, 0)  # Darker green outline
    else:
        fill_color = (200, 0, 0)  # Red = Stopped
        outline_color = (150, 0, 0)  # Darker red outline
    
    # Draw shield shape (rounded top, pointed bottom)
    shield_points = [
        (width // 2, 8),           # Top center
        (width - 12, 12),          # Top right
        (width - 8, 20),            # Upper right
        (width - 8, height - 16),  # Lower right
        (width // 2, height - 4),  # Bottom point
        (8, height - 16),          # Lower left
        (8, 20),                    # Upper left
        (12, 12),                   # Top left
    ]
    
    # Draw the shield with fill and outline
    dc.polygon(shield_points, fill=fill_color, outline=outline_color, width=2)
    
    # Draw rounded top arc for more realistic shield look
    dc.arc([8, 8, width - 8, 24], start=0, end=180, fill=outline_color, width=2)
    
    # Save the image
    os.makedirs("icons", exist_ok=True)
    image.save(f"icons/{filename}", "PNG")
    print(f"[+] Created: icons/{filename}")

if __name__ == "__main__":
    create_shield_icon("green", "shield_green.png")
    create_shield_icon("red", "shield_red.png")
    print("\n[+] Icon files created successfully!")

