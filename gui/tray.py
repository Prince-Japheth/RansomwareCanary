"""System tray GUI interface."""

import sys
import threading
import os
from pathlib import Path

try:
    import pystray
    from PIL import Image, ImageDraw
    PYSRAY_AVAILABLE = True
except ImportError:
    PYSRAY_AVAILABLE = False
    # Fallback to tkinter if pystray not available
    try:
        import tkinter as tk
        from tkinter import messagebox
        TKINTER_AVAILABLE = True
    except ImportError:
        TKINTER_AVAILABLE = False


class SystemTrayApp:
    """System tray application with start/stop protection controls."""
    
    def __init__(self, start_callback, stop_callback):
        """
        Initialize the system tray app.
        
        Args:
            start_callback: Function to call when starting protection
            stop_callback: Function to call when stopping protection
        """
        self.start_callback = start_callback
        self.stop_callback = stop_callback
        self.icon = None
        self.running = False
    
    def create_image(self, color):
        """
        Generate a simple shield icon dynamically.
        
        Args:
            color: "green" for active, "red" for stopped
        
        Returns:
            PIL Image object
        """
        # Generate a simple shield icon dynamically
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        
        # Draw a dark background (shield-ish)
        dc.rectangle((0, 0, width, height), fill=(30, 30, 30))
        
        # Draw colored circle
        if color == "green":
            fill_color = (0, 255, 0)  # Green = Active/Protected
        else:
            fill_color = (255, 0, 0)  # Red = Stopped
        
        dc.ellipse((10, 10, 54, 54), fill=fill_color)
        
        return image
    
    def on_clicked(self, icon, item):
        """Handle menu item clicks."""
        item_text = str(item)
        
        if item_text == "Start Protection":
            self.running = True
            self.update_icon_state()
            # Run the monitoring in a separate thread so GUI doesn't freeze
            threading.Thread(target=self.start_callback, daemon=True).start()
        elif item_text == "Stop Protection":
            self.running = False
            self.update_icon_state()
            self.stop_callback()
        elif item_text == "Exit":
            self.stop_callback()
            icon.stop()
            sys.exit(0)
    
    def update_icon_state(self):
        """Update the icon based on current state."""
        if self.icon:
            if self.running:
                self.icon.icon = self.create_image("green")  # Green = Safe/Active
                self.icon.title = "Ransomware Canary: ACTIVE"
            else:
                self.icon.icon = self.create_image("red")  # Red = Stopped
                self.icon.title = "Ransomware Canary: STOPPED"
    
    def run(self):
        """Start the system tray icon."""
        if not PYSRAY_AVAILABLE:
            print("[-] ERROR: pystray not available. Install with: pip install pystray Pillow")
            print("[-] Falling back to console mode...")
            # Just run the start callback directly
            self.start_callback()
            return
        
        # Define the menu
        menu = pystray.Menu(
            pystray.MenuItem(
                "Start Protection",
                self.on_clicked,
                checked=lambda item: self.running,
                default=True if not self.running else False
            ),
            pystray.MenuItem(
                "Stop Protection",
                self.on_clicked,
                checked=lambda item: not self.running,
                default=True if self.running else False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.on_clicked)
        )
        
        # Create icon with initial red (stopped) state
        self.icon = pystray.Icon(
            "Ransomware Canary",
            self.create_image("red"),
            "Ransomware Canary: STOPPED",
            menu
        )
        
        # Run the icon (this blocks)
        self.icon.run()


class TrayIcon:
    """System tray icon interface for the canary system."""
    
    def __init__(self, detector, logger=None):
        """
        Initialize the tray icon.
        
        Args:
            detector: RansomwareDetector instance
            logger: ThreatLogger instance
        """
        self.detector = detector
        self.logger = logger
        self.icon = None
        self.status = "protected"  # "protected" or "threat_stopped"
        self.threat_count = 0
        
        if not PYSRAY_AVAILABLE and not TKINTER_AVAILABLE:
            self.logger.log_error("No GUI library available. Running in headless mode.")
    
    def _create_icon_image(self, color="green"):
        """
        Create an icon image with the specified color.
        
        Args:
            color: "green" for protected, "red" for threat stopped
        """
        # Create a simple colored circle icon
        width = height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        if color == "green":
            fill_color = (0, 255, 0)  # Green
        else:
            fill_color = (255, 0, 0)  # Red
        
        # Draw a circle
        margin = 8
        draw.ellipse(
            [margin, margin, width - margin, height - margin],
            fill=fill_color,
            outline=(0, 0, 0),
            width=2
        )
        
        return image
    
    def update_status(self, status, threat_count=0):
        """
        Update the tray icon status.
        
        Args:
            status: "protected" or "threat_stopped"
            threat_count: Number of threats neutralized
        """
        self.status = status
        self.threat_count = threat_count
        
        if self.icon:
            color = "red" if status == "threat_stopped" else "green"
            self.icon.icon = self._create_icon_image(color)
            self.icon.title = self._get_tooltip()
    
    def _get_tooltip(self):
        """Get the tooltip text for the tray icon."""
        if self.status == "threat_stopped":
            return f"Ransomware Canary - ATTACK STOPPED! ({self.threat_count} threats neutralized)"
        return "Ransomware Canary - Protected"
    
    def _on_threat_detected(self):
        """Callback when a threat is detected."""
        self.update_status("threat_stopped", self.threat_count + 1)
    
    def _create_menu(self):
        """Create the context menu for the tray icon."""
        return pystray.Menu(
            pystray.MenuItem(
                "Status: Protected" if self.status == "protected" else f"Status: Threat Stopped ({self.threat_count})",
                None,
                enabled=False
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self._on_exit)
        )
    
    def _on_exit(self, icon, item):
        """Handle exit menu item."""
        if self.detector:
            self.detector.stop_monitoring()
        if self.logger:
            self.logger.log_info("Ransomware Canary stopped by user")
        icon.stop()
        sys.exit(0)
    
    def run(self):
        """Start the tray icon in a separate thread."""
        if not PYSRAY_AVAILABLE:
            # Fallback to simple console mode
            self._run_console_mode()
            return
        
        # Create initial icon
        icon_image = self._create_icon_image("green")
        
        self.icon = pystray.Icon(
            "RansomwareCanary",
            icon_image,
            self._get_tooltip(),
            self._create_menu()
        )
        
        # Run in a separate thread
        icon_thread = threading.Thread(target=self.icon.run, daemon=True)
        icon_thread.start()
    
    def _run_console_mode(self):
        """Fallback console mode when GUI libraries are not available."""
        if self.logger:
            self.logger.log_info("Running in console mode (GUI libraries not available)")
        # Just keep the main thread alive
        # The detector runs in its own thread


class SimpleTkinterGUI:
    """Simple tkinter window as fallback if pystray is not available."""
    
    def __init__(self, detector, logger=None):
        """Initialize the tkinter GUI."""
        self.detector = detector
        self.logger = logger
        self.root = None
        self.status_label = None
        self.threat_count = 0
    
    def create_window(self):
        """Create the main window."""
        self.root = tk.Tk()
        self.root.title("Ransomware Canary - Zero-Infrastructure Endpoint Protection")
        self.root.geometry("400x200")
        
        # Status frame
        status_frame = tk.Frame(self.root, bg="green", padx=20, pady=20)
        status_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = tk.Label(
            status_frame,
            text="🛡️ PROTECTED",
            font=("Arial", 24, "bold"),
            bg="green",
            fg="white"
        )
        self.status_label.pack(expand=True)
        
        # Info label
        info_label = tk.Label(
            self.root,
            text="Monitoring bait files for unauthorized access",
            font=("Arial", 10),
            pady=10
        )
        info_label.pack()
        
        # Threat count
        self.threat_label = tk.Label(
            self.root,
            text="Threats neutralized: 0",
            font=("Arial", 10)
        )
        self.threat_label.pack()
        
        # Exit button
        exit_button = tk.Button(
            self.root,
            text="Exit",
            command=self._on_exit,
            padx=20,
            pady=5
        )
        exit_button.pack(pady=10)
    
    def update_status(self, status, threat_count=0):
        """Update the GUI status."""
        self.threat_count = threat_count
        
        if status == "threat_stopped":
            self.status_label.config(
                text="⚡ ATTACK STOPPED!",
                bg="red"
            )
            self.status_label.master.config(bg="red")
            self.threat_label.config(text=f"Threats neutralized: {threat_count}")
            # Show alert
            messagebox.showwarning(
                "THREAT DETECTED",
                f"Ransomware activity detected and neutralized!\n\n"
                f"Total threats stopped: {threat_count}"
            )
        else:
            self.status_label.config(
                text="🛡️ PROTECTED",
                bg="green"
            )
            self.status_label.master.config(bg="green")
    
    def _on_exit(self):
        """Handle exit."""
        if self.detector:
            self.detector.stop_monitoring()
        if self.logger:
            self.logger.log_info("Ransomware Canary stopped by user")
        self.root.quit()
        self.root.destroy()
    
    def run(self):
        """Run the GUI main loop."""
        if not TKINTER_AVAILABLE:
            return
        
        self.create_window()
        self.root.mainloop()

