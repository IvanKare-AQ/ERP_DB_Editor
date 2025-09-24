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

from src.gui.main_window import MainWindow


def main():
    """Main entry point for the ERP Database Editor application."""
    # Set the appearance mode and color theme
    ctk.set_appearance_mode("system")  # Modes: "System" (standard), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
    # Create and run the main application
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
