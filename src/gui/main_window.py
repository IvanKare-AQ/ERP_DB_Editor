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
from src.gui.edit_panel import EditPanel


class MainWindow:
    """Main application window for the ERP Database Editor."""
    
    def __init__(self):
        """Initialize the main window."""
        self.root = ctk.CTk()
        self.root.title("ERP Database Editor")
        self.root.geometry("1800x1000")  # Even wider to ensure edit panel visibility
        self.root.minsize(1400, 800)  # Increased minimum width and height
        
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
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(10, 0))
        
        # Create toolbar
        self.create_toolbar()
        
        # Create main content area
        self.create_content_area()
        
        # Create status bar
        self.create_status_bar()
        
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
        
        # Separator
        separator2 = ctk.CTkFrame(self.toolbar_frame, width=2, height=30)
        separator2.pack(side="left", padx=10, pady=5)
        
        # Filter controls
        self.filter_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Filter Data",
            command=self.open_filter_dialog,
            width=100,
            state="disabled"
        )
        self.filter_button.pack(side="left", padx=5, pady=5)
        
        self.clear_filters_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Clear Filters",
            command=self.clear_all_filters,
            width=100,
            state="disabled"
        )
        self.clear_filters_button.pack(side="left", padx=5, pady=5)
        
        # Multi-selection control section
        self.clear_user_erp_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Clear User ERP Name",
            command=self.clear_user_erp_names,
            width=140,
            state="disabled"
        )
        self.clear_user_erp_button.pack(side="left", padx=5, pady=5)
        
    def create_content_area(self):
        """Create the main content area with tree view and edit panel."""
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)
        
        # Create right panel for editing first (to ensure it gets space)
        self.right_panel = ctk.CTkScrollableFrame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", padx=(5, 10), pady=10)
        self.right_panel.configure(width=700, fg_color=("gray90", "gray15"))  # Fixed width with distinct color
        
        # Create left panel for tree view
        self.left_panel = ctk.CTkFrame(self.content_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # Create tree view widget
        self.tree_view = TreeViewWidget(self.left_panel)
        self.tree_view.pack(fill="both", expand=True)
        
        # Bind tree view selection event
        self.tree_view.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Create edit panel
        self.edit_panel = EditPanel(self.right_panel, self.tree_view, self)
        self.edit_panel.pack(fill="both", expand=True)
        
        # Load column visibility settings
        self.tree_view.load_column_visibility(self.config_manager)
        
        # Update Save View button state
        self.update_save_view_button_state()
        
        # Refresh AI models after main window is fully initialized
        if hasattr(self.edit_panel, 'refresh_models_on_startup'):
            self.root.after(1000, self.edit_panel.refresh_models_on_startup)  # Delay to ensure everything is loaded
        
    def create_status_bar(self):
        """Create the status bar at the bottom of the application."""
        # Create status bar frame at the bottom of the main window
        self.status_bar = ctk.CTkFrame(self.root)
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=(0, 10))
        
        # Create status label
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
        
        # Create file info label on the right
        self.file_info_label = ctk.CTkLabel(
            self.status_bar,
            text="No file loaded",
            font=ctk.CTkFont(size=12),
            anchor="e"
        )
        self.file_info_label.pack(side="right", padx=10, pady=5)
    
    def update_status(self, message):
        """Update the status bar message."""
        self.status_label.configure(text=message)
        self.root.update_idletasks()  # Force immediate update
    
    def update_file_info(self, file_path=None):
        """Update the file information in the status bar."""
        if file_path:
            filename = os.path.basename(file_path)
            self.file_info_label.configure(text=f"File: {filename}")
        else:
            self.file_info_label.configure(text="No file loaded")
        
    def open_file(self):
        """Open an Excel file."""
        file_path = filedialog.askopenfilename(
            title="Open Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.update_status("Loading file...")
                
                # Load the Excel file
                self.excel_handler.load_file(file_path)
                self.current_file_path = file_path
                
                # Update tree view with data
                self.tree_view.load_data(self.excel_handler.get_data())
                
                # Load saved filters after data is loaded
                saved_filters = self.config_manager.get_filters()
                if saved_filters:
                    self.tree_view.load_filters(saved_filters)
                
                # Update Save View button state after loading data and filters
                self.update_save_view_button_state()
                
                # Enable buttons
                self.save_button.configure(state="normal")
                self.save_as_button.configure(state="normal")
                self.column_visibility_button.configure(state="normal")
                self.save_view_button.configure(state="normal")
                self.filter_button.configure(state="normal")
                self.clear_filters_button.configure(state="normal")
                
                # Update status and file info
                self.update_status("File loaded successfully")
                self.update_file_info(file_path)
                
            except Exception as e:
                self.update_status("Error loading file")
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
                
    def save_file(self):
        """Save the current file."""
        if self.current_file_path:
            try:
                self.update_status("Saving file...")
                
                # Get data with user modifications applied
                data = self.get_data_with_modifications()
                self.excel_handler.save_file(self.current_file_path, data)
                
                self.update_status("File saved successfully")
            except Exception as e:
                self.update_status("Error saving file")
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
                    self.update_status("Saving file...")
                    
                    # Get data with user modifications applied
                    data = self.get_data_with_modifications()
                    self.excel_handler.save_file(file_path, data)
                    self.current_file_path = file_path
                    
                    self.update_status("File saved successfully")
                    self.update_file_info(file_path)
                except Exception as e:
                    self.update_status("Error saving file")
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
            
            # Get current filters from tree view
            current_filters = self.tree_view.get_current_filters()
            
            # Save column visibility to config
            self.config_manager.save_column_visibility(visible_columns)
            
            # Save filters to config
            self.config_manager.save_filters(current_filters)
            
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
        
        # Check if current filters differ from saved filters
        current_filters = self.tree_view.get_current_filters()
        saved_filters = self.config_manager.get_filters()
        
        # Compare current and saved visibility
        visibility_changed = False
        if current_visibility and saved_visibility:
            visibility_changed = set(current_visibility) != set(saved_visibility)
        else:
            visibility_changed = bool(current_visibility) and not bool(saved_visibility)
        
        # Compare current and saved filters
        filters_changed = False
        if current_filters and saved_filters:
            filters_changed = current_filters != saved_filters
        else:
            filters_changed = bool(current_filters) and not bool(saved_filters)
        
        # Update button state
        has_changes = visibility_changed or filters_changed
        if has_changes:
            self.save_view_button.configure(state="normal")
            self.view_has_changes = True
        else:
            self.save_view_button.configure(state="disabled")
            self.view_has_changes = False
    
    def open_filter_dialog(self):
        """Open the filter dialog."""
        if hasattr(self, 'tree_view') and self.tree_view.has_data():
            self.update_status("Opening filter dialog...")
            from src.gui.filter_dialog import FilterDialog
            dialog = FilterDialog(self.root, self.tree_view, self)
            self.root.wait_window(dialog.dialog)
            self.update_status("Ready")
        else:
            messagebox.showwarning("Warning", "Please open a file first")
    
    def clear_all_filters(self):
        """Clear all active filters."""
        if hasattr(self, 'tree_view') and self.tree_view.has_data():
            self.tree_view.clear_all_filters()
            # Notify that filters have changed
            self.view_has_changes = True
            self.update_save_view_button_state()
            self.update_status("All filters cleared")
        else:
            messagebox.showwarning("Warning", "Please open a file first")
    
    def clear_user_erp_names(self):
        """Clear User ERP Name for all selected items."""
        if hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items:
            cleared_count = self.tree_view.clear_user_erp_names_for_selected()
            if cleared_count > 0:
                self.update_status(f"Cleared User ERP Name for {cleared_count} items")
            else:
                self.update_status("No User ERP Name values to clear")
        else:
            self.update_status("Please select items first")
    
    def on_tree_select(self, event):
        """Handle tree view selection events."""
        selection = self.tree_view.tree.selection()
        if selection:
            # Get all ERP items from selection
            erp_items = []
            for item in selection:
                tags = self.tree_view.tree.item(item, "tags")
                if tags and len(tags) >= 2 and tags[0] in ["erp_item", "erp_item_even", "erp_item_odd"]:
                    row_id = tags[1]
                    original_data = self.get_original_row_data(row_id)
                    if original_data:
                        erp_items.append((original_data, row_id))
            
            if erp_items:
                # If only one ERP item selected, populate edit panel
                if len(erp_items) == 1:
                    original_data, row_id = erp_items[0]
                    self.edit_panel.set_selected_item(original_data, row_id)
                    erp_name = original_data.get('ERP name', 'Unknown')
                    self.update_status(f"Selected: {erp_name}")
                else:
                    # Multiple ERP items selected
                    self.edit_panel.set_selected_item(None, None)
                    self.update_status(f"Selected {len(erp_items)} items")
                
                # Store selected items for multi-selection operations
                self.tree_view.selected_items = erp_items
                
                # Enable clear button if we have ERP items selected
                self.clear_user_erp_button.configure(state="normal")
            else:
                # No ERP items selected
                self.edit_panel.set_selected_item(None, None)
                self.tree_view.selected_items = []
                self.clear_user_erp_button.configure(state="disabled")
                self.update_status("Ready")
        else:
            self.edit_panel.set_selected_item(None, None)
            self.tree_view.selected_items = []
            self.clear_user_erp_button.configure(state="disabled")
    
    def find_row_id_from_tree_item(self, item_text, item_values):
        """Find the row ID for a tree item."""
        # This is a simplified approach - in a real implementation,
        # you might want to store row IDs in tree items
        if not self.tree_view.data.empty:
            # Find matching row in data
            matching_rows = self.tree_view.data[
                (self.tree_view.data['ERP name'] == item_text)
            ]
            if not matching_rows.empty:
                row = matching_rows.iloc[0]
                return f"{row.get('ERP name', '')}_{row.get('Article Category', '')}_{row.get('Article Subcategory', '')}_{row.get('Article Sublevel', '')}"
        return None
    
    def get_original_row_data(self, row_id):
        """Get original row data for a row ID."""
        if not self.tree_view.data.empty:
            # Parse row ID to find matching data
            parts = row_id.split('_')
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sublevel = parts[3]
                
                # Use the clean column name (without duplicates)
                sublevel_col = 'Article Sublevel '
                matching_rows = self.tree_view.data[
                    (self.tree_view.data['ERP name'] == erp_name) &
                    (self.tree_view.data['Article Category'] == category) &
                    (self.tree_view.data['Article Subcategory'] == subcategory) &
                    (self.tree_view.data[sublevel_col] == sublevel)
                ]
                if not matching_rows.empty:
                    return matching_rows.iloc[0].to_dict()
        return None
    
    def get_data_with_modifications(self):
        """Get data with user modifications applied."""
        import pandas as pd
        
        # Start with original data
        data = self.tree_view.get_data().copy()
        
        # Clean up duplicate columns - keep only the first occurrence of each column
        columns_to_keep = []
        seen_columns = set()
        
        for col in data.columns:
            base_name = col.split('_')[0] if '_' in col else col
            if base_name not in seen_columns:
                columns_to_keep.append(col)
                seen_columns.add(base_name)
        
        # Filter data to keep only unique columns
        data = data[columns_to_keep]
        
        # Ensure User ERP Name column exists and is positioned correctly
        if 'User ERP Name' in data.columns:
            # If column exists but is in wrong position, move it
            current_pos = data.columns.get_loc('User ERP Name')
            erp_name_pos = data.columns.get_loc('ERP name')
            
            # If User ERP Name is not right after ERP name, move it
            if current_pos != erp_name_pos + 1:
                # Remove the column from its current position
                user_erp_values = data['User ERP Name'].copy()
                data = data.drop('User ERP Name', axis=1)
                
                # Insert it right after ERP name
                erp_name_pos = data.columns.get_loc('ERP name') + 1
                data.insert(erp_name_pos, 'User ERP Name', user_erp_values)
        else:
            # If column doesn't exist, add it after ERP name
            erp_name_pos = data.columns.get_loc('ERP name') + 1
            data.insert(erp_name_pos, 'User ERP Name', '')
        
        # Apply user modifications
        modifications = self.tree_view.get_user_modifications()
        
        for row_id, mods in modifications.items():
            # Find the row in data
            parts = row_id.split('_')
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sublevel = parts[3]
                
                # Use the clean column name (without duplicates)
                sublevel_col = 'Article Sublevel '
                # Find matching row
                mask = (
                    (data['ERP name'] == erp_name) &
                    (data['Article Category'] == category) &
                    (data['Article Subcategory'] == subcategory) &
                    (data[sublevel_col] == sublevel)
                )
                
                if mask.any():
                    # Apply User ERP Name modification
                    if 'user_erp_name' in mods:
                        data.loc[mask, 'User ERP Name'] = mods['user_erp_name']
                    
                    # Apply reassignment modifications
                    if 'new_category' in mods and 'new_subcategory' in mods and 'new_sublevel' in mods:
                        data.loc[mask, 'Article Category'] = mods['new_category']
                        data.loc[mask, 'Article Subcategory'] = mods['new_subcategory']
                        data.loc[mask, sublevel_col] = mods['new_sublevel']
        
        return data
            
    def run(self):
        """Run the main application loop."""
        self.root.mainloop()
