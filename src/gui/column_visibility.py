"""
Column Visibility Dialog for ERP Database Editor
Allows users to control which columns are visible in the tree view.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class ColumnVisibilityDialog:
    """Dialog for managing column visibility settings."""
    
    def __init__(self, parent, tree_view, config_manager, main_window=None):
        """Initialize the column visibility dialog."""
        self.parent = parent
        self.tree_view = tree_view
        self.config_manager = config_manager
        self.main_window = main_window
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Column Visibility")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Column visibility states
        self.column_states = {}
        
        # Setup the dialog
        self.setup_dialog()
        
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")
        
    def setup_dialog(self):
        """Setup the dialog components."""
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Column Visibility Settings", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 10))
        
        # Instructions
        instructions_label = ctk.CTkLabel(main_frame, 
                                       text="Select which columns should be visible in the tree view:")
        instructions_label.pack(pady=(0, 10))
        
        # Scrollable frame for checkboxes
        self.scrollable_frame = ctk.CTkScrollableFrame(main_frame, height=300)
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create checkboxes for each column
        self.create_column_checkboxes()
        
        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons
        self.apply_button = ctk.CTkButton(button_frame, text="Apply", 
                                        command=self.apply_changes, width=100)
        self.apply_button.pack(side="left", padx=(0, 10))
        
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel", 
                                         command=self.cancel_dialog, width=100)
        self.cancel_button.pack(side="left")
        
    def create_column_checkboxes(self):
        """Create checkboxes for each column."""
        # Get all available columns from tree view (this is the definitive list)
        # This includes User ERP Name, Image, ERP Name, CAD Name, etc.
        all_columns = self.tree_view.tree["columns"]
        
        # Get currently visible columns from tree view (not from saved config)
        currently_visible = self.tree_view.get_visible_columns()
        
        for column in all_columns:
            # Create frame for each checkbox
            checkbox_frame = ctk.CTkFrame(self.scrollable_frame)
            checkbox_frame.pack(fill="x", pady=2)
            
            # Create checkbox
            var = tk.BooleanVar()
            
            # Set initial state based on current tree view state
            if currently_visible:
                var.set(column in currently_visible)
            else:
                var.set(True)  # Default to visible if no visibility settings
                
            self.column_states[column] = var
            
            checkbox = ctk.CTkCheckBox(checkbox_frame, text=column, variable=var)
            checkbox.pack(side="left", padx=10, pady=5)
            
    def apply_changes(self):
        """Apply the column visibility changes."""
        # Get selected columns
        visible_columns = [col for col, var in self.column_states.items() if var.get()]
        
        # Apply to tree view only (don't save to config)
        self.tree_view.set_visible_columns(visible_columns)
        
        # Notify main window that view has changed
        if self.main_window:
            self.main_window.view_has_changes = True
        
        # Close dialog
        self.dialog.destroy()
        
    def cancel_dialog(self):
        """Cancel the dialog without applying changes."""
        self.dialog.destroy()
