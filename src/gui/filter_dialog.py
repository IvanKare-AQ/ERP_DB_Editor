"""
Filter Dialog for ERP Database Editor
Allows users to apply filters to columns similar to Excel spreadsheet filters.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk


class FilterDialog:
    """Dialog for managing column filters."""

    # Width constants for consistent UI sizing
    SCROLLABLE_FRAME_HEIGHT = 350  # Height for scrollable frame
    APPLY_BUTTON_WIDTH = 120       # Width for apply button
    CLEAR_BUTTON_WIDTH = 100       # Width for clear button
    CANCEL_BUTTON_WIDTH = 100      # Width for cancel button
    COLUMN_LABEL_WIDTH = 120       # Width for column labels
    FILTER_TYPE_WIDTH = 100        # Width for filter type dropdown
    FILTER_VALUE_WIDTH = 200       # Width for filter value input
    CLEAR_FILTER_WIDTH = 60        # Width for clear filter button

    # Height constants for consistent UI sizing
    CLEAR_FILTER_HEIGHT = 20       # Height for clear filter button

    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the filter dialog."""
        self.parent = parent
        self.tree_view = tree_view
        self.main_window = main_window
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Filter Data")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Filter controls
        self.filter_controls = {}
        self.available_columns = [
            "User ERP Name", "ERP Name", "CAD Name", "Electronics", "Product Value", 
            "Manufacturer", "SKU", "EAN 13", "Unit", "Supplier", 
            "Expiry Date", "Tracking Method", "Procurement Method", "Remark"
        ]
        
        # Setup the dialog
        self.setup_dialog()
        
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
    def setup_dialog(self):
        """Setup the dialog components."""
        # Main frame
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="Filter Data", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(0, 10))
        
        # Instructions
        instructions_label = ctk.CTkLabel(main_frame, 
                                       text="Set filters for columns. Leave empty to show all values.")
        instructions_label.pack(pady=(0, 10))
        
        # Scrollable frame for filter controls
        self.scrollable_frame = ctk.CTkScrollableFrame(main_frame, height=self.SCROLLABLE_FRAME_HEIGHT)
        self.scrollable_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        # Create filter controls for each column
        self.create_filter_controls()
        
        # Button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        # Buttons
        self.apply_button = ctk.CTkButton(button_frame, text="Apply Filters",
                                        command=self.apply_filters, width=self.APPLY_BUTTON_WIDTH)
        self.apply_button.pack(side="left", padx=(0, 10))
        
        self.clear_button = ctk.CTkButton(button_frame, text="Clear All",
                                        command=self.clear_all, width=self.CLEAR_BUTTON_WIDTH)
        self.clear_button.pack(side="left", padx=(0, 10))
        
        self.cancel_button = ctk.CTkButton(button_frame, text="Cancel",
                                         command=self.cancel_dialog, width=self.CANCEL_BUTTON_WIDTH)
        self.cancel_button.pack(side="left")
        
    def create_filter_controls(self):
        """Create filter controls for each column."""
        for column in self.available_columns:
            # Create frame for each column filter
            filter_frame = ctk.CTkFrame(self.scrollable_frame)
            filter_frame.pack(fill="x", pady=2)
            
            # Column label
            column_label = ctk.CTkLabel(filter_frame, text=column, width=self.COLUMN_LABEL_WIDTH)
            column_label.pack(side="left", padx=10, pady=5)
            
            # Filter type dropdown
            filter_type_var = tk.StringVar(value="contains")
            filter_type_dropdown = ctk.CTkOptionMenu(
                filter_frame, 
                values=["contains", "equals", "starts with", "ends with"],
                variable=filter_type_var,
                width=self.FILTER_TYPE_WIDTH
            )
            filter_type_dropdown.pack(side="left", padx=5, pady=5)
            
            # Filter value entry
            filter_value_var = tk.StringVar()
            filter_value_entry = ctk.CTkEntry(
                filter_frame, 
                placeholder_text="Filter value...",
                textvariable=filter_value_var,
                width=self.FILTER_VALUE_WIDTH
            )
            filter_value_entry.pack(side="left", padx=5, pady=5)
            
            # Clear filter button
            clear_filter_button = ctk.CTkButton(
                filter_frame,
                text="Clear",
                command=lambda col=column: self.clear_column_filter(col),
                width=self.CLEAR_FILTER_WIDTH,
                height=self.CLEAR_FILTER_HEIGHT
            )
            clear_filter_button.pack(side="left", padx=5, pady=5)
            
            # Store filter controls
            self.filter_controls[column] = {
                'type': filter_type_var,
                'value': filter_value_var,
                'clear_button': clear_filter_button
            }
            
            # Load current filter value if exists
            if column in self.tree_view.active_filters:
                filter_info = self.tree_view.active_filters[column]
                filter_value_var.set(filter_info['value'])
                filter_type_var.set(filter_info['type'].replace('_', ' '))
    
    def clear_column_filter(self, column):
        """Clear filter for a specific column."""
        if column in self.filter_controls:
            self.filter_controls[column]['value'].set('')
            self.filter_controls[column]['type'].set('contains')
    
    def apply_filters(self):
        """Apply all filters to the tree view."""
        # Clear existing filters
        self.tree_view.clear_all_filters()
        
        # Apply new filters
        for column, controls in self.filter_controls.items():
            filter_value = controls['value'].get().strip()
            filter_type = controls['type'].get().replace(' ', '_')
            
            if filter_value:  # Only apply if there's a value
                self.tree_view.apply_filter(column, filter_value, filter_type)
        
        # Notify main window that filters have changed
        if self.main_window:
            self.main_window.view_has_changes = True
            self.main_window.update_save_view_button_state()
        
        # Close dialog
        self.dialog.destroy()
    
    def clear_all(self):
        """Clear all filter values."""
        for controls in self.filter_controls.values():
            controls['value'].set('')
            controls['type'].set('contains')
    
    def cancel_dialog(self):
        """Cancel the dialog without applying changes."""
        self.dialog.destroy()
