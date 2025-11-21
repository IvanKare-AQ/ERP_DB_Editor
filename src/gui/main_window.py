"""
Main Window for ERP Database Editor
Contains the main application window with menu, toolbar, and tree view.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import pandas as pd

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.backend.json_handler import JsonHandler
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
        
        # Ensure consistent font rendering across platforms
        self.configure_fonts()
        
        # Initialize backend components
        self.json_handler = JsonHandler()
        self.config_manager = ConfigManager()
        
        # Current file path
        self.current_file_path = self.json_handler.file_path
        
        # Track view changes
        self.view_has_changes = False
        # Track data changes for Save button state
        self.data_has_changes = False
        
        # Setup the GUI
        self.setup_gui()
        
        # Load database on startup
        self.load_database()
    
    def configure_fonts(self):
        """Configure fonts for consistent rendering across platforms."""
        import tkinter as tk
        
        try:
            # Set default font sizes for consistent rendering across platforms
            default_font = tk.font.nametofont("TkDefaultFont")
            default_font.configure(size=11)
            
            text_font = tk.font.nametofont("TkTextFont")
            text_font.configure(size=11)
            
            fixed_font = tk.font.nametofont("TkFixedFont")
            fixed_font.configure(size=11)
            
            # Note: CustomTkinter doesn't have set_default_font method
            # Font configuration is handled per widget
        except Exception as e:
            print(f"Warning: Could not configure fonts: {e}")
            # Continue without font configuration if it fails
        
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
        self.save_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Save",
            command=self.save_database,
            width=100,
            state="disabled"
        )
        self.save_button.pack(side="left", padx=5, pady=5)
        
        self.export_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Export",
            command=self.export_to_excel,
            width=100,
            state="disabled"
        )
        self.export_button.pack(side="left", padx=5, pady=5)
        
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
        
        # View toggle button (New Items / Current Items)
        self.view_toggle_button = ctk.CTkButton(
            self.toolbar_frame,
            text="Current Items",
            command=self.toggle_view,
            width=120,
            state="disabled"
        )
        self.view_toggle_button.pack(side="left", padx=5, pady=5)
        self._showing_new_items = False
        
        
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
        self.tree_view = TreeViewWidget(self.left_panel, self.config_manager)
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
        if hasattr(self, 'status_label'):
            self.status_label.configure(text=message)
        if hasattr(self, 'root'):
            self.root.update_idletasks()  # Force immediate update
    
    def update_file_info(self, file_path=None):
        """Update the file information in the status bar."""
        if file_path:
            filename = os.path.basename(file_path)
            self.file_info_label.configure(text=f"File: {filename}")
        else:
            self.file_info_label.configure(text="No file loaded")
        
    def load_database(self):
        """Load the component database from JSON."""
        try:
            self.update_status("Loading database...")
            
            # Load the JSON file
            self.json_handler.load_file()
            
            # Load categories
            self.json_handler.load_categories()
            
            # Enrich data with category properties
            self.json_handler.enrich_data()
            # Load added items (for Add Item functionality in Manual tab)
            self.json_handler.load_added_items()
            
            # Update tree view with data and categories
            self.tree_view.load_data(self.json_handler.get_data(), self.json_handler.get_categories())
            # Initialize with added data
            self.tree_view.set_added_data(self.json_handler.get_added_data())
            
            # Load saved filters after data is loaded
            saved_filters = self.config_manager.get_filters()
            if saved_filters:
                self.tree_view.load_filters(saved_filters)
            
            # Update Save View button state after loading data and filters
            self.update_save_view_button_state()
            
            # Enable buttons (Save button stays disabled until changes are made)
            self.save_button.configure(state="disabled")
            self.export_button.configure(state="normal")
            self.column_visibility_button.configure(state="normal")
            self.save_view_button.configure(state="normal")
            self.filter_button.configure(state="normal")
            self.clear_filters_button.configure(state="normal")
            self.view_toggle_button.configure(state="normal")
            
            # Update status and file info
            self.update_status("Database loaded successfully")
            self.update_file_info(self.json_handler.file_path)
            
        except Exception as e:
            self.update_status("Error loading database")
            messagebox.showerror("Error", f"Failed to load database: {str(e)}")
    
    def refresh_added_items_view(self):
        """Synchronize the tree view with the latest draft items."""
        if not hasattr(self, 'tree_view'):
            return
        # Ensure added items are loaded
        self.json_handler.load_added_items()
        self.tree_view.set_added_data(self.json_handler.get_added_data())
        # Update view if currently showing new items
        if self._showing_new_items:
            self.tree_view.show_added_items()
    
    def toggle_view(self):
        """Toggle between New Items and Current Items view."""
        if not hasattr(self, 'tree_view'):
            return
        
        self._showing_new_items = not self._showing_new_items
        
        if self._showing_new_items:
            self.tree_view.show_added_items()
            self.view_toggle_button.configure(text="New Items")
            self.update_status("Viewing new items")
        else:
            self.tree_view.show_primary_items()
            self.view_toggle_button.configure(text="Current Items")
            self.update_status("Viewing current items")
            
    def mark_data_changed(self):
        """Mark that data has been changed, enabling Save button."""
        self.data_has_changes = True
        if hasattr(self, 'save_button'):
            self.save_button.configure(state="normal")
    
    def save_database(self):
        """Save the database to JSON."""
        try:
            self.update_status("Saving database...")
            
            # Get data with user modifications applied
            data = self.get_data_with_modifications()
            self.json_handler.save_file(data=data)
            
            # Reset data changes flag and disable Save button
            self.data_has_changes = False
            self.save_button.configure(state="disabled")
            
            self.update_status("Database saved successfully")
        except Exception as e:
            self.update_status("Error saving database")
            messagebox.showerror("Error", f"Failed to save database: {str(e)}")
    
    def export_to_excel(self):
        """Export all data (filtered and unfiltered) to Excel file."""
        try:
            # Get file path from user
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Export to Excel"
            )
            
            if not file_path:
                self.update_status("Export cancelled")
                return
            
            self.update_status("Exporting to Excel...")
            
            # Get all data with user modifications applied
            data = self.get_data_with_modifications()
            
            # Create a copy for export (we'll modify ERP Name for Excel)
            export_data = data.copy()
            
            # Convert ERP Name objects to full_name strings for Excel
            if 'ERP Name' in export_data.columns:
                import pandas as pd
                def get_erp_full_name(erp_obj):
                    if isinstance(erp_obj, dict):
                        return erp_obj.get('full_name', '')
                    elif pd.isna(erp_obj):
                        return ''
                    else:
                        return str(erp_obj)
                
                export_data['ERP Name'] = export_data['ERP Name'].apply(get_erp_full_name)
            
            # Export to Excel using openpyxl
            try:
                import openpyxl
                from openpyxl import Workbook
            except ImportError:
                messagebox.showerror("Error", "openpyxl is required for Excel export. Please install it: pip install openpyxl")
                self.update_status("Export failed: openpyxl not installed")
                return
            
            # Use pandas to_excel method
            export_data.to_excel(file_path, index=False, engine='openpyxl')
            
            self.update_status(f"Data exported successfully to {os.path.basename(file_path)}")
            messagebox.showinfo("Export Successful", f"Data exported successfully to:\n{file_path}")
            
        except Exception as e:
            self.update_status("Error exporting to Excel")
            messagebox.showerror("Error", f"Failed to export to Excel: {str(e)}")
            
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
                    erp_name_obj = original_data.get('ERP Name', {})
                    erp_name = erp_name_obj.get('full_name', 'Unknown') if isinstance(erp_name_obj, dict) else str(erp_name_obj) if erp_name_obj else 'Unknown'
                    self.update_status(f"Selected: {erp_name}")
                else:
                    # Multiple ERP items selected
                    self.edit_panel.manual_editor.set_selected_item(None, None)
                    self.update_status(f"Selected {len(erp_items)} items")
                
                # Store selected items for multi-selection operations
                self.tree_view.selected_items = erp_items
                
                # Update apply to selected button state
                if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                    self.edit_panel.ai_editor.update_apply_to_selected_button_state()
            else:
                # No ERP items selected
                self.edit_panel.manual_editor.set_selected_item(None, None)
                self.tree_view.selected_items = []
                if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                    self.edit_panel.ai_editor.update_apply_to_selected_button_state()
                self.update_status("Ready")
        else:
            self.edit_panel.manual_editor.set_selected_item(None, None)
            self.tree_view.selected_items = []
            if hasattr(self, 'edit_panel') and hasattr(self.edit_panel, 'ai_editor') and hasattr(self.edit_panel.ai_editor, 'update_apply_to_selected_button_state'):
                self.edit_panel.ai_editor.update_apply_to_selected_button_state()
    
    def find_row_id_from_tree_item(self, item_text, item_values):
        """Find the row ID for a tree item."""
        dataset = self.tree_view.get_data_with_modifications()
        if dataset is None or dataset.empty:
            dataset = self.tree_view.get_data()
        if dataset is None or dataset.empty:
            return None
        
        import pandas as pd
        def get_erp_full_name(erp_obj):
            if isinstance(erp_obj, dict):
                return erp_obj.get('full_name', '')
            elif pd.isna(erp_obj):
                return ''
            else:
                return str(erp_obj)
        
        erp_name_series = dataset['ERP Name'].apply(get_erp_full_name)
        matching_rows = dataset[(erp_name_series == item_text)]
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            delimiter = getattr(self.tree_view, 'ROW_ID_DELIMITER', "◆◆◆")
            erp_name_obj = row.get('ERP Name', {})
            erp_name_full = get_erp_full_name(erp_name_obj)
            return f"{erp_name_full}{delimiter}{row.get('Category', '')}{delimiter}{row.get('Subcategory', '')}{delimiter}{row.get('Sub-subcategory', '')}"
        return None
    
    def get_original_row_data(self, row_id):
        """Get original row data for a row ID, with user modifications applied."""
        dataset = self.tree_view.get_data()
        if dataset is not None and not dataset.empty:
            # Parse base row ID (original location) to find matching data
            delimiter = getattr(self.tree_view, 'ROW_ID_DELIMITER', "◆◆◆")
            base_row_id = row_id
            entry = self.tree_view.user_modifications.get(row_id)
            if entry and '_base_row_id' in entry:
                base_row_id = entry['_base_row_id']
            parts = base_row_id.split(delimiter)
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sub_subcategory = parts[3]
                
                # Use the clean column name (without duplicates)
                sub_subcategory_col = 'Sub-subcategory'
                # Extract full_name from ERP name object for comparison
                import pandas as pd
                def get_erp_full_name(erp_obj):
                    if isinstance(erp_obj, dict):
                        return erp_obj.get('full_name', '')
                    elif pd.isna(erp_obj):
                        return ''
                    else:
                        return str(erp_obj)
                
                erp_name_series = dataset['ERP Name'].apply(get_erp_full_name)
                matching_rows = dataset[
                    (erp_name_series == erp_name) &
                    (dataset['Category'] == category) &
                    (dataset['Subcategory'] == subcategory) &
                    (dataset[sub_subcategory_col] == sub_subcategory)
                ]
                if not matching_rows.empty:
                    row_data = matching_rows.iloc[0].to_dict()
                    
                    # Apply buffered modifications to the row data for preview
                    mods = self.tree_view.user_modifications.get(row_id, {})
                    if mods:
                        if 'erp_name' in mods and mods['erp_name']:
                            row_data['ERP Name'] = mods['erp_name']
                        if 'manufacturer' in mods:
                            row_data['Manufacturer'] = mods['manufacturer']
                        if 'remark' in mods:
                            row_data['Remark'] = mods['remark']
                        if 'image' in mods:
                            row_data['Image'] = mods['image']
                        if 'new_category' in mods:
                            row_data['Category'] = mods['new_category']
                        if 'new_subcategory' in mods:
                            row_data['Subcategory'] = mods['new_subcategory']
                        if 'new_sub_subcategory' in mods:
                            row_data['Sub-subcategory'] = mods['new_sub_subcategory']
                    
                    return row_data
        return None
    
    def get_data_with_modifications(self):
        """Get data with user modifications applied."""
        import pandas as pd
        
        base_data = self.tree_view.get_data()
        if base_data is None:
            return pd.DataFrame()
        data = base_data.copy()
        
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
        
        # Apply user modifications
        modifications = self.tree_view.get_user_modifications()
        
        for row_id, mods in modifications.items():
            # Find the row in data using the original row identifier
            delimiter = getattr(self.tree_view, 'ROW_ID_DELIMITER', "◆◆◆")
            base_row_id = mods.get('_base_row_id', row_id)
            parts = base_row_id.split(delimiter)
            if len(parts) >= 4:
                erp_name = parts[0]
                category = parts[1]
                subcategory = parts[2]
                sub_subcategory = parts[3]
                
                # Use the clean column name (without duplicates)
                sub_subcategory_col = 'Sub-subcategory'
                # Find matching row - extract full_name from ERP name object for comparison
                def get_erp_full_name(erp_obj):
                    if isinstance(erp_obj, dict):
                        return erp_obj.get('full_name', '')
                    elif pd.isna(erp_obj):
                        return ''
                    else:
                        return str(erp_obj)
                
                erp_name_series = data['ERP Name'].apply(get_erp_full_name)
                mask = (
                    (erp_name_series == erp_name) &
                    (data['Category'] == category) &
                    (data['Subcategory'] == subcategory) &
                    (data[sub_subcategory_col] == sub_subcategory)
                )
                
                if mask.any():
                    # Apply ERP name modification
                    if 'erp_name' in mods and mods['erp_name']:
                        # Ensure ERP name column is object dtype to handle dict values
                        if data['ERP Name'].dtype != 'object':
                            data['ERP Name'] = data['ERP Name'].astype('object')
                        # Create a copy of the dict to avoid reference issues
                        import copy
                        erp_name_obj = mods['erp_name']
                        # Validate that it's a dict with required keys
                        if isinstance(erp_name_obj, dict):
                            erp_name_obj = copy.deepcopy(erp_name_obj)
                            # Ensure all required keys exist
                            if 'full_name' not in erp_name_obj:
                                erp_name_obj['full_name'] = ''
                            if 'type' not in erp_name_obj:
                                erp_name_obj['type'] = ''
                            if 'part_number' not in erp_name_obj:
                                erp_name_obj['part_number'] = ''
                            if 'additional_parameters' not in erp_name_obj:
                                erp_name_obj['additional_parameters'] = ''
                        # Assign the dict object directly - iterate to ensure proper assignment
                        for idx in data[mask].index:
                            data.at[idx, 'ERP Name'] = erp_name_obj
                    
                    # Apply Manufacturer modification
                    if 'manufacturer' in mods:
                        data.loc[mask, 'Manufacturer'] = mods['manufacturer']
                    
                    # Apply Remark modification
                    if 'remark' in mods:
                        data.loc[mask, 'Remark'] = mods['remark']
                    
                    # Apply Image modification
                    if 'image' in mods:
                        data.loc[mask, 'Image'] = mods['image']
                    
                    # Apply reassignment modifications
                    if 'new_category' in mods and 'new_subcategory' in mods and 'new_sub_subcategory' in mods:
                        data.loc[mask, 'Category'] = mods['new_category']
                        data.loc[mask, 'Subcategory'] = mods['new_subcategory']
                        data.loc[mask, sub_subcategory_col] = mods['new_sub_subcategory']
        
        return data
    
    def convert_multiline_cells(self):
        """Convert multiline cells to single line entries."""
        if not hasattr(self, 'json_handler') or self.json_handler is None:
            messagebox.showwarning("Warning", "No data loaded.")
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
            result = self.json_handler.convert_multiline_to_single_line()
            
            # Reload the tree view with the updated data from JSON handler
            self.tree_view.load_data(self.json_handler.get_data())
            
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
        if not hasattr(self, 'json_handler') or self.json_handler is None:
            messagebox.showwarning("Warning", "No data loaded.")
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
            result = self.json_handler.remove_nen_prefix()
            
            # Reload the tree view with the updated data from JSON handler
            self.tree_view.load_data(self.json_handler.get_data())
            
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
    
    def run(self):
        """Run the main application loop."""
        self.root.mainloop()
