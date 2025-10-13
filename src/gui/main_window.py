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
        self.root.geometry("2000x1000")  # Even wider to ensure edit panel visibility with wider tabs
        self.root.minsize(1600, 800)  # Increased minimum width and height for wider tabs
        
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
        
        # Separator after Clear Filters
        separator3 = ctk.CTkFrame(self.toolbar_frame, width=2, height=30)
        separator3.pack(side="left", padx=10, pady=5)
        
        # Multi-selection control section
        self.clear_user_erp_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Clear User ERP Name",
            command=self.clear_user_erp_names,
            width=140,
            state="disabled"
        )
        self.clear_user_erp_button.pack(side="left", padx=5, pady=5)
        
        self.apply_user_erp_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Apply User ERP Names",
            command=self.apply_user_erp_names,
            width=150,
            state="disabled"
        )
        self.apply_user_erp_button.pack(side="left", padx=5, pady=5)
        
        # Separator after Apply User ERP Names
        separator4 = ctk.CTkFrame(self.toolbar_frame, width=2, height=30)
        separator4.pack(side="left", padx=10, pady=5)
        
        
    def create_content_area(self):
        """Create the main content area with tree view and edit panel."""
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Create right panel for editing first (to ensure it gets space)
        self.right_panel = ctk.CTkFrame(self.content_frame)
        self.right_panel.pack(side="right", fill="both", padx=(5, 10), pady=10)
        # Use the same width as the EditPanel for consistency
        self.right_panel.configure(width=EditPanel.get_panel_width())

        # Create left panel for tree view
        self.left_panel = ctk.CTkFrame(self.content_frame)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Create tree view widget
        self.tree_view = TreeViewWidget(self.left_panel)
        self.tree_view.pack(fill="both", expand=True)

        # Bind tree view selection event
        self.tree_view.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Create edit panel with tabs
        self.edit_panel = EditPanel(self.right_panel, self.tree_view, self)
        self.edit_panel.pack(fill="both", expand=True)

        # Load column visibility settings
        self.tree_view.load_column_visibility(self.config_manager)

        # Update Save View button state
        self.update_save_view_button_state()


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
                self.apply_user_erp_button.configure(state="normal")
                
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
            
            # Get current AI model and prompt from AI editor
            selected_model = None
            selected_prompt = None
            if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor'):
                selected_model = self.edit_panel.ai_editor.model_dropdown.get() if hasattr(self.edit_panel.ai_editor, 'model_dropdown') else None
                selected_prompt = getattr(self.edit_panel.ai_editor, 'selected_prompt', None)
            
            # Save column visibility to config
            self.config_manager.save_column_visibility(visible_columns)
            
            # Save filters to config
            self.config_manager.save_filters(current_filters)
            
            # Save AI model if available and not "No models available"
            if selected_model and selected_model != "No models available":
                self.config_manager.save_selected_model(selected_model)
            
            # Save AI prompt if available
            if selected_prompt:
                self.config_manager.save_selected_prompt(selected_prompt)
            
            # Reset view changes flag
            self.view_has_changes = False
            self.update_save_view_button_state()
            
            # Update status
            self.update_status("View settings saved successfully (including AI model and prompt)")
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
        
        # Check if current AI model differs from saved model
        current_model = None
        if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'model_dropdown'):
            current_model = self.edit_panel.ai_editor.model_dropdown.get()
            if current_model == "No models available":
                current_model = None

        saved_model = self.config_manager.get_selected_model()

        # Check if current AI prompt differs from saved prompt
        current_prompt = None
        if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor'):
            current_prompt = getattr(self.edit_panel.ai_editor, 'selected_prompt', None)
        saved_prompt = self.config_manager.get_selected_prompt()
        
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
        
        # Compare current and saved AI model
        model_changed = current_model != saved_model

        # Compare current and saved AI prompt
        prompt_changed = current_prompt != saved_prompt
        
        # Update button state
        has_changes = visibility_changed or filters_changed or model_changed or prompt_changed
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
                # If only one ERP item selected, populate manual edit panel
                if len(erp_items) == 1:
                    original_data, row_id = erp_items[0]
                    self.edit_panel.manual_editor.set_selected_item(original_data, row_id)
                    erp_name = original_data.get('ERP name', 'Unknown')
                    self.update_status(f"Selected: {erp_name}")
                else:
                    # Multiple ERP items selected
                    self.edit_panel.manual_editor.set_selected_item(None, None)
                    self.update_status(f"Selected {len(erp_items)} items")
                
                # Store selected items for multi-selection operations
                self.tree_view.selected_items = erp_items
                
                # Enable clear button if we have ERP items selected
                self.clear_user_erp_button.configure(state="normal")
                
                # Update apply to selected button state
                if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                    self.edit_panel.ai_editor.update_apply_to_selected_button_state()
            else:
                # No ERP items selected
                self.edit_panel.manual_editor.set_selected_item(None, None)
                self.tree_view.selected_items = []
                self.clear_user_erp_button.configure(state="disabled")
                if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                    self.edit_panel.ai_editor.update_apply_to_selected_button_state()
                self.update_status("Ready")
        else:
            self.manual_edit_panel.set_selected_item(None, None)
            self.tree_view.selected_items = []
            self.clear_user_erp_button.configure(state="disabled")
            if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                self.edit_panel.ai_editor.update_apply_to_selected_button_state()
    
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
                delimiter = "◆◆◆"
                return f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{row.get('Article Sublevel', '')}"
        return None
    
    def get_original_row_data(self, row_id):
        """Get original row data for a row ID."""
        if hasattr(self.tree_view, 'data') and not self.tree_view.data.empty:
            # Parse row ID to find matching data
            parts = row_id.split('◆◆◆')
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sublevel = parts[3]
                
                # Use the clean column name (without duplicates)
                sublevel_col = 'Article Sublevel'
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
            # Remove trailing spaces to identify duplicate columns
            base_name = col.strip()
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
            parts = row_id.split('◆◆◆')
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sublevel = parts[3]
                
                # Use the clean column name (without duplicates)
                sublevel_col = 'Article Sublevel'
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
                    
                    # Apply Manufacturer modification
                    if 'manufacturer' in mods:
                        data.loc[mask, 'Manufacturer'] = mods['manufacturer']
                    
                    # Apply REMARK modification
                    if 'remark' in mods:
                        data.loc[mask, 'REMARK'] = mods['remark']
                    
                    # Apply reassignment modifications
                    if 'new_category' in mods and 'new_subcategory' in mods and 'new_sublevel' in mods:
                        data.loc[mask, 'Article Category'] = mods['new_category']
                        data.loc[mask, 'Article Subcategory'] = mods['new_subcategory']
                        data.loc[mask, sublevel_col] = mods['new_sublevel']
        
        return data
    
    def convert_multiline_cells(self):
        """Convert multiline cells to single line entries."""
        if not hasattr(self, 'excel_handler') or self.excel_handler is None:
            messagebox.showwarning("Warning", "No data loaded. Please open an Excel file first.")
            return
        
        # Show confirmation dialog
        response = messagebox.askyesno(
            "Convert Multiline Cells", 
            "This will convert all multiline cells to single line entries.\n\n"
            "Multiline content will be converted to single lines with spaces.\n"
            "This operation cannot be undone.\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            self.update_status("Multiline conversion cancelled")
            return
        
        # Show progress
        self.update_status("Converting multiline cells to single line...")
        
        # Perform the conversion
        try:
            result = self.excel_handler.convert_multiline_to_single_line()
            
            # Reload the tree view with the updated data from Excel handler
            self.tree_view.load_data(self.excel_handler.get_data())
            
            # Update status with results
            if result["converted"] > 0:
                self.update_status(
                    f"Converted {result['converted']} multiline cells to single line "
                    f"({result['percentage']:.1f}% of total cells)"
                )
                messagebox.showinfo(
                    "Conversion Complete", 
                    f"Successfully converted {result['converted']} multiline cells to single line.\n\n"
                    f"Total cells processed: {result['total_cells']}\n"
                    f"Percentage converted: {result['percentage']:.1f}%"
                )
            else:
                self.update_status("No multiline cells found to convert")
                messagebox.showinfo("No Conversion Needed", "No multiline cells were found in the data.")
                
        except Exception as e:
            error_msg = f"Error converting multiline cells: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("Conversion Error", error_msg)
    
    def remove_nen_prefix(self):
        """Remove 'NEN' prefix and subsequent spaces from all cells."""
        if not hasattr(self, 'excel_handler') or self.excel_handler is None:
            messagebox.showwarning("Warning", "No data loaded. Please open an Excel file first.")
            return
        
        # Show confirmation dialog
        response = messagebox.askyesno(
            "Remove NEN Prefix", 
            "This will remove 'NEN' prefix and subsequent spaces from all cells.\n\n"
            "This operation cannot be undone.\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            self.update_status("NEN removal cancelled")
            return
        
        # Show progress
        self.update_status("Removing 'NEN' prefix from cells...")
        
        # Perform the removal
        try:
            result = self.excel_handler.remove_nen_prefix()
            
            # Reload the tree view with the updated data from Excel handler
            self.tree_view.load_data(self.excel_handler.get_data())
            
            # Update status with results
            if result["converted"] > 0:
                self.update_status(
                    f"Removed 'NEN' prefix from {result['converted']} cells "
                    f"({result['percentage']:.1f}% of total cells)"
                )
                messagebox.showinfo(
                    "NEN Removal Complete", 
                    f"Successfully removed 'NEN' prefix from {result['converted']} cells.\n\n"
                    f"Total cells processed: {result['total_cells']}\n"
                    f"Percentage converted: {result['percentage']:.1f}%"
                )
            else:
                self.update_status("No cells with 'NEN' prefix found")
                messagebox.showinfo("No NEN Prefix Found", "No cells starting with 'NEN' were found in the data.")
                
        except Exception as e:
            error_msg = f"Error removing 'NEN' prefix: {str(e)}"
            self.update_status(error_msg)
            messagebox.showerror("NEN Removal Error", error_msg)
    
    def apply_user_erp_names(self):
        """Apply User ERP Name values to ERP name column (move operation)."""
        if not hasattr(self, 'excel_handler') or self.excel_handler is None:
            messagebox.showwarning("Warning", "No data loaded. Please open an Excel file first.")
            return
        
        # Get current data with modifications
        data = self.get_data_with_modifications()
        if data is None:
            messagebox.showerror("Error", "No data available to process.")
            return
        
        # Check for User ERP Names in both user modifications and original data
        user_modifications = self.tree_view.get_user_modifications()
        
        # Create a set to track rows that have User ERP Names (avoid double counting)
        rows_with_user_erp_names = set()
        
        # Count User ERP Names from user modifications
        for row_id, mods in user_modifications.items():
            if 'user_erp_name' in mods and mods['user_erp_name'].strip():
                rows_with_user_erp_names.add(row_id)
        
        # Count User ERP Names from original data (excluding rows already counted in modifications)
        if 'User ERP Name' in data.columns:
            for index, row in data.iterrows():
                user_erp_name = row.get('User ERP Name', '').strip()
                if user_erp_name:
                    # Create row_id for this row to check if it's already in user modifications
                    erp_name = row.get('ERP name', '')
                    category = row.get('Article Category', '')
                    subcategory = row.get('Article Subcategory', '')
                    sublevel = row.get('Article Sublevel', '')
                    
                    if erp_name and category and subcategory:
                        row_id = f"{erp_name}◆◆◆{category}◆◆◆{subcategory}◆◆◆{sublevel}"
                        if row_id not in rows_with_user_erp_names:
                            rows_with_user_erp_names.add(row_id)
        
        user_erp_names_count = len(rows_with_user_erp_names)
        
        if user_erp_names_count == 0:
            messagebox.showinfo("Info", "No User ERP Names found to apply.")
            self.update_status("No User ERP Names to apply")
            return
        
        # Show confirmation dialog
        response = messagebox.askyesno(
            "Apply User ERP Names", 
            f"This will permanently move {user_erp_names_count} User ERP Name values to the ERP name column.\n\n"
            "This operation will:\n"
            "• Replace existing ERP name values with User ERP Name values\n"
            "• Clear the User ERP Name column\n"
            "• Cannot be undone without reloading the file\n\n"
            "Do you want to continue?"
        )
        
        if not response:
            self.update_status("Apply User ERP Names cancelled")
            return
        
        try:
            self.update_status("Applying User ERP Names...")
            
            # Get current data with modifications
            data = self.get_data_with_modifications()
            if data is None:
                messagebox.showerror("Error", "No data available to process.")
                return
            
            # Apply the move operation
            moved_count = 0
            
            # First, handle User ERP Names from user modifications
            for row_id, mods in user_modifications.items():
                if 'user_erp_name' in mods and mods['user_erp_name'].strip():
                    # Parse row_id to find the original row
                    parts = row_id.split('◆◆◆')
                    if len(parts) >= 4:
                        erp_name = parts[0]
                        category = parts[1]
                        subcategory = parts[2]
                        sublevel = parts[3]
                        
                        # Find matching row
                        mask = (
                            (data['ERP name'] == erp_name) &
                            (data['Article Category'] == category) &
                            (data['Article Subcategory'] == subcategory) &
                            (data['Article Sublevel'] == sublevel)
                        )
                        
                        if mask.any():
                            # Move User ERP Name to ERP name
                            data.loc[mask, 'ERP name'] = mods['user_erp_name']
                            # Clear User ERP Name
                            data.loc[mask, 'User ERP Name'] = ''
                            moved_count += 1
            
            # Then, handle User ERP Names from original data
            if 'User ERP Name' in data.columns:
                # Find rows with non-empty User ERP Name values
                user_erp_mask = data['User ERP Name'].fillna('').str.strip().ne('')
                
                if user_erp_mask.any():
                    # Move User ERP Name values to ERP name for these rows
                    data.loc[user_erp_mask, 'ERP name'] = data.loc[user_erp_mask, 'User ERP Name']
                    # Clear User ERP Name column
                    data.loc[user_erp_mask, 'User ERP Name'] = ''
                    moved_count += user_erp_mask.sum()
            
            # Clear user modifications for user_erp_name
            for row_id in user_modifications:
                if 'user_erp_name' in user_modifications[row_id]:
                    del user_modifications[row_id]['user_erp_name']
            
            # Update the Excel handler with the new data
            self.excel_handler.data = data
            
            # Reload the tree view with updated data
            self.tree_view.load_data(data)
            
            # Update status
            self.update_status(f"Successfully applied {moved_count} User ERP Names to ERP name column")
            messagebox.showinfo("Success", f"Successfully applied {moved_count} User ERP Names to the ERP name column.\n\nThe User ERP Name column has been cleared.")
            
        except Exception as e:
            self.update_status("Error applying User ERP Names")
            messagebox.showerror("Error", f"Failed to apply User ERP Names: {str(e)}")
            
    def run(self):
        """Run the main application loop."""
        self.root.mainloop()
