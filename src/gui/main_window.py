"""
Main Window for ERP Database Editor
Contains the main application window with menu, toolbar, and tree view.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.backend.excel_handler import ExcelHandler
from src.backend.config_manager import ConfigManager
from src.gui.tree_view import TreeViewWidget
from src.gui.column_visibility import ColumnVisibilityDialog


class MainWindow:
    """Main application window for the ERP Database Editor."""
    
    def __init__(self):
        """Initialize the main window."""
        self.root = ctk.CTk()
        self.root.title("ERP Database Editor")
        self.root.geometry("1200x800")
        
        # Initialize backend components
        self.excel_handler = ExcelHandler()
        self.config_manager = ConfigManager()
        
        # Current file path
        self.current_file_path = None
        
        # Track view changes
        self.view_has_changes = False
        
        # Setup the GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI components."""
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        self.create_content_area()
        
    def create_toolbar(self):
        """Create the toolbar with file operations and view controls."""
        self.toolbar_frame = ctk.CTkFrame(self.main_frame)
        self.toolbar_frame.pack(fill="x", pady=(0, 10))
        
        # File operations
        self.open_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Open Excel",
            command=self.open_file,
            width=100
        )
        self.open_button.pack(side="left", padx=5, pady=5)
        
        self.save_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Save",
            command=self.save_file,
            width=100,
            state="disabled"
        )
        self.save_button.pack(side="left", padx=5, pady=5)
        
        self.save_as_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Save As",
            command=self.save_as_file,
            width=100,
            state="disabled"
        )
        self.save_as_button.pack(side="left", padx=5, pady=5)
        
        # Separator
        separator = ctk.CTkFrame(self.toolbar_frame, width=2, height=30)
        separator.pack(side="left", padx=10, pady=5)
        
        # View controls
        self.column_visibility_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Column Visibility",
            command=self.open_column_visibility,
            width=150,
            state="disabled"
        )
        self.column_visibility_button.pack(side="left", padx=5, pady=5)
        
        self.save_view_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Save View",
            command=self.save_view,
            width=100,
            state="disabled"
        )
        self.save_view_button.pack(side="left", padx=5, pady=5)
        
    def create_content_area(self):
        """Create the main content area with tree view."""
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Create tree view widget
        self.tree_view = TreeViewWidget(self.content_frame)
        self.tree_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load column visibility settings
        self.tree_view.load_column_visibility(self.config_manager)
        
        # Update Save View button state
        self.update_save_view_button_state()
        
    def open_file(self):
        """Open an Excel file."""
        file_path = filedialog.askopenfilename(
            title="Open Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                # Load the Excel file
                self.excel_handler.load_file(file_path)
                self.current_file_path = file_path
                
                # Update tree view with data
                self.tree_view.load_data(self.excel_handler.get_data())
                
                # Enable buttons
                self.save_button.configure(state="normal")
                self.save_as_button.configure(state="normal")
                self.column_visibility_button.configure(state="normal")
                self.save_view_button.configure(state="normal")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def save_file(self):
        """Save the current file."""
        if self.current_file_path:
            try:
                # Get data from tree view
                data = self.tree_view.get_data()
                self.excel_handler.save_file(self.current_file_path, data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No file is currently open")
            
    def save_as_file(self):
        """Save the current file with a new name."""
        if self.current_file_path:
            file_path = filedialog.asksaveasfilename(
                title="Save As",
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
            )
            
            if file_path:
                try:
                    # Get data from tree view
                    data = self.tree_view.get_data()
                    self.excel_handler.save_file(file_path, data)
                    self.current_file_path = file_path
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save file: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No file is currently open")
            
    def open_column_visibility(self):
        """Open the column visibility dialog."""
        if hasattr(self, 'tree_view') and self.tree_view.has_data():
            dialog = ColumnVisibilityDialog(self.root, self.tree_view, self.config_manager, self)
            self.root.wait_window(dialog.dialog)
            # Update Save View button state after dialog closes
            self.update_save_view_button_state()
        else:
            messagebox.showwarning("Warning", "Please open a file first")
            
    def save_view(self):
        """Save the current view settings."""
        try:
            # Get current column visibility from tree view
            visible_columns = self.tree_view.get_visible_columns()
            
            # Save to config
            self.config_manager.save_column_visibility(visible_columns)
            
            # Reset view changes flag
            self.view_has_changes = False
            self.update_save_view_button_state()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save view: {str(e)}")
    
    def update_save_view_button_state(self):
        """Update the Save View button state based on whether there are unsaved changes."""
        if not hasattr(self, 'save_view_button'):
            return
            
        # Check if current view differs from saved settings
        current_visibility = self.tree_view.get_visible_columns()
        saved_visibility = self.config_manager.get_column_visibility()
        
        # Compare current and saved visibility
        if current_visibility and saved_visibility:
            has_changes = set(current_visibility) != set(saved_visibility)
        else:
            has_changes = bool(current_visibility) and not bool(saved_visibility)
        
        # Update button state
        if has_changes:
            self.save_view_button.configure(state="normal")
            self.view_has_changes = True
        else:
            self.save_view_button.configure(state="disabled")
            self.view_has_changes = False
            
    def run(self):
        """Run the main application loop."""
        self.root.mainloop()
