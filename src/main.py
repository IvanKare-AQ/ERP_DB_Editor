"""
ERP Database Editor - Main Application
A Python GUI application for editing ERP database files using CustomTkinter.
"""

import customtkinter as ctk
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Import with proper path handling for PyInstaller
try:
    from src.gui.main_window import MainWindow
except ImportError:
    # Fallback for PyInstaller
    from gui.main_window import MainWindow


def main():
    """Main entry point for the ERP Database Editor application."""
    # Set the appearance mode and color theme
    ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    # Set default font sizes for consistent rendering across platforms
    import tkinter as tk
    default_font = tk.font.nametofont("TkDefaultFont")
    default_font.configure(size=11)
    
    text_font = tk.font.nametofont("TkTextFont")
    text_font.configure(size=11)
    
    fixed_font = tk.font.nametofont("TkFixedFont")
    fixed_font.configure(size=11)
    
    # Set CustomTkinter default font
    ctk.set_default_font("Arial", 11)
    
    # Create and run the main application
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
