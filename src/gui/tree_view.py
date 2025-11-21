"""
Tree View Widget for ERP Database Editor
Displays data in hierarchical tree format with Category, Subcategory, and Sub-subcategory.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd


class TreeViewWidget(ctk.CTkFrame):
    """Tree view widget for displaying hierarchical ERP data."""
    
    ROW_ID_DELIMITER = "◆◆◆"
    
    def __init__(self, parent, config_manager=None):
        """Initialize the tree view widget."""
        super().__init__(parent)
        
        # Data storage
        self.data = None
        self.primary_data = None
        self.categories = None
        self.visible_columns = None
        self.filtered_data = None
        self.active_filters = {}
        self.primary_columns = []
        self.added_data = pd.DataFrame()
        self.current_view = "primary"
        self._mod_version = 0
        self._modified_cache = None
        self._filtered_cache = None
        self._base_data_id = None
        
        # User modifications tracking
        self.user_modifications = {}
        self.selected_item = None
        self.selected_items = []  # For multi-selection support
        
        # Config manager for saving visibility settings
        self.config_manager = config_manager
        
        # Columns will be dynamically determined from loaded data
        self._all_columns = None
        
        # Create the tree view
        self.create_tree_view()

    # ------------------------------------------------------------------
    # Helpers for user modifications and row IDs
    # ------------------------------------------------------------------
    def _ensure_mod_entry(self, row_id):
        """Ensure a modification entry exists for the given row ID."""
        entry = self.user_modifications.setdefault(row_id, {})
        entry.setdefault('_base_row_id', row_id)
        return entry

    def _get_mod_entry(self, row_id):
        return self.user_modifications.get(row_id)

    def _get_base_row_id(self, row_id):
        entry = self.user_modifications.get(row_id)
        if entry and '_base_row_id' in entry:
            return entry['_base_row_id']
        return row_id

    def _parse_row_id(self, row_id):
        parts = row_id.split(self.ROW_ID_DELIMITER)
        while len(parts) < 4:
            parts.append('')
        return parts[0], parts[1], parts[2], parts[3]

    def _build_row_id(self, erp_name, category, subcategory, sub_subcategory):
        return f"{erp_name}{self.ROW_ID_DELIMITER}{category}{self.ROW_ID_DELIMITER}{subcategory}{self.ROW_ID_DELIMITER}{sub_subcategory}"

    def _invalidate_caches(self):
        self._modified_cache = None
        self._filtered_cache = None

    def _invalidate_filtered_cache(self):
        self._filtered_cache = None

    def _mark_data_dirty(self):
        self._mod_version += 1
        self._invalidate_caches()
        
    def create_tree_view(self):
        """Create the tree view component."""
        # Create frame for tree view and scrollbars
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Create tree view with custom styling
        self.tree = ttk.Treeview(self.tree_frame)
        
        # Create scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        
        # Configure tree view
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Configure tree view styling
        self.configure_tree_style()
        
        # Pack components
        self.tree.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        
        # Configure columns
        self.setup_columns()
        
        # Force style refresh for Windows compatibility
        self.refresh_tree_style()
    
    def configure_tree_style(self):
        """Configure the tree view styling with dark mode colors and fonts."""
        # Create a style object
        style = ttk.Style()
        
        # Set the theme to ensure proper styling on all platforms
        try:
            # Try to set a theme that works well with custom styling
            available_themes = style.theme_names()
            if 'clam' in available_themes:
                style.theme_use('clam')
            elif 'alt' in available_themes:
                style.theme_use('alt')
        except:
            pass  # Use default theme if setting fails
        
        # Configure the treeview style with dark theme
        style.configure("Treeview", 
                       font=("Arial", 11),  # Consistent font size
                       rowheight=24,  # Increased row height for better readability
                       background="#2b2b2b",  # Dark background
                       foreground="#ffffff",  # White text
                       fieldbackground="#2b2b2b")  # Dark field background
        
        # Configure treeview heading with dark theme
        style.configure("Treeview.Heading",
                       font=("Arial", 11, "bold"),  # Bold headers with consistent font
                       background="#3c3c3c",  # Darker header background
                       foreground="#ffffff")  # White header text
        
        # Additional configuration for Windows compatibility
        style.map("Treeview.Heading",
                 background=[('active', '#4c4c4c'),
                           ('pressed', '#5c5c5c')])
        
        style.map("Treeview",
                 background=[('selected', '#1976d2')],
                 foreground=[('selected', '#ffffff')])
    
    def refresh_tree_style(self):
        """Force refresh the tree style for Windows compatibility."""
        try:
            # Force a style refresh by temporarily changing and restoring the theme
            style = ttk.Style()
            current_theme = style.theme_use()
            style.theme_use('clam')
            style.theme_use(current_theme)
            
            # Re-apply the styling
            self.configure_tree_style()
        except:
            pass  # Ignore errors during style refresh
        
        # Define dark color schemes for different hierarchy levels
        self.hierarchy_colors = {
            'category': '#404040',      # Dark gray for categories
            'subcategory': '#4a4a4a',   # Slightly lighter gray for subcategories  
            'sub_subcategory': '#545454',      # Even lighter gray for sub-subcategories
            'erp_item': '#2b2b2b'       # Dark background for ERP items
        }
        
        # Configure tags for different hierarchy levels with dark theme
        self.tree.tag_configure('category', 
                               background=self.hierarchy_colors['category'],
                               font=("Arial", 10, "bold"),
                               foreground="#64b5f6")  # Light blue text
        
        self.tree.tag_configure('subcategory',
                               background=self.hierarchy_colors['subcategory'], 
                               font=("Arial", 9, "bold"),
                               foreground="#ba68c8")  # Light purple text
        
        self.tree.tag_configure('sub_subcategory',
                               background=self.hierarchy_colors['sub_subcategory'],
                               font=("Arial", 9, "bold"),
                               foreground="#81c784")  # Light green text
        
        self.tree.tag_configure('erp_item',
                               background=self.hierarchy_colors['erp_item'],
                               font=("Arial", 9),
                               foreground="#ffffff")  # White text
        
        # Configure alternating row backgrounds for ERP items
        self.tree.tag_configure('erp_item_odd',
                               background="#2b2b2b",  # Dark background
                               font=("Arial", 9),
                               foreground="#ffffff")
        
        self.tree.tag_configure('erp_item_even',
                               background="#333333",  # Slightly lighter dark background
                               font=("Arial", 9),
                               foreground="#ffffff")
        
        # Configure selection colors for dark theme
        self.tree.tag_configure('selected',
                               background="#1976d2",  # Blue selection
                               foreground="#ffffff")
        
        # Add hover effect for dark theme
        self.tree.tag_configure('hover',
                               background="#424242")  # Dark hover background
        
        # Bind mouse events for hover effects
        self.tree.bind("<Motion>", self.on_mouse_motion)
        self.tree.bind("<Leave>", self.on_mouse_leave)
        
    def setup_columns(self):
        """Setup the tree view columns."""
        # Get columns from data (or fallback)
        columns = self.get_all_columns()
        self.tree["columns"] = columns
        
        # Configure column headings dynamically
        self.tree.heading("#0", text="Hierarchy", anchor="w")
        for col in columns:
            self.tree.heading(col, text=col)
        
        # Configure column widths
        self.tree.column("#0", width=200, minwidth=150)
        for col in columns:
            self.tree.column(col, width=100, minwidth=80)
            
    def load_data(self, data, categories=None, set_primary=True):
        """Load data into the tree view."""
        data_to_use = pd.DataFrame() if data is None else data.copy(deep=True)
        self.data = data_to_use
        if set_primary:
            self.primary_data = data_to_use.copy(deep=True)
            self.primary_columns = list(data_to_use.columns)
            self.current_view = "primary"
        self.categories = categories if categories is not None else self.categories
        self._base_data_id = id(self.data)
        self._mark_data_dirty()
        
        # Extract columns from data (source of truth)
        if self.data is not None and not self.data.empty:
            # Get all columns from the data
            data_columns = list(self.data.columns)
            
            # Map data column names to display names
            display_columns = []
            for col in data_columns:
                # Map internal column names to display names
                display_name = self.get_display_column_name(col)
                if display_name not in display_columns:
                    display_columns.append(display_name)
            
            self._all_columns = tuple(display_columns)
        else:
            # Fallback if no data
            fallback_columns = self.primary_columns if self.primary_columns else []
            self._all_columns = tuple(fallback_columns)
        
        # Update tree columns to match data
        # If visibility settings exist, use them; otherwise use all columns
        if self.visible_columns:
            self.setup_columns_with_visibility(self.visible_columns)
        else:
            self.setup_columns()
        
        # Clear filters when loading new data
        self.active_filters.clear()
        self.refresh_view()
            
    def clear_tree(self):
        """Clear all items from the tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def populate_tree(self, data):
        """Populate the tree with hierarchical data."""
        if self.categories:
            # Use loaded categories to build the tree
            self._populate_tree_from_categories(data, self.categories)
        else:
            # Fallback to grouping by data columns if no categories loaded
            self._populate_tree_from_data(data)
            
    def _populate_tree_from_data(self, data):
        """Populate the tree by grouping data columns."""
        if 'Category' not in data.columns:
            return
        
        # Group by Category
        categories = data.groupby('Category')
        
        for category_name, category_data in categories:
            # Create category node with color tag
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=self._get_empty_values(),
                                           tags=("category",))
            
            # Group by Subcategory within category
            subcategories = category_data.groupby('Subcategory')
            
            for subcategory_name, subcategory_data in subcategories:
                # Create subcategory node with color tag
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=self._get_empty_values(),
                                                  tags=("subcategory",))
                
                # Group by Sub-subcategory within subcategory
                sub_subcategories = subcategory_data.groupby('Sub-subcategory')
                
                for sub_subcategory_name, sub_subcategory_data in sub_subcategories:
                    # Create sub-subcategory node with color tag
                    sub_subcategory_node = self.tree.insert(subcategory_node, "end", 
                                                           text=sub_subcategory_name,
                                                           values=self._get_empty_values(),
                                                           tags=("sub_subcategory",))
                    
                    # Add ERP Name items under sub-subcategory with alternating backgrounds
                    erp_items = list(sub_subcategory_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        self._insert_erp_item(sub_subcategory_node, row, index)

    def _populate_tree_from_categories(self, data, categories):
        """Populate the tree using the categories structure."""
        for category in categories:
            category_name = category.get('category', '')
            if not category_name:
                continue
                
            # Create category node
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=self._get_empty_values(),
                                           tags=("category",))
            
            # Filter data for this category
            category_data = data[data['Category'] == category_name]
            
            subcategories = category.get('subcategories', [])
            for sub in subcategories:
                subcategory_name = sub.get('name', '')
                if not subcategory_name:
                    continue
                    
                # Create subcategory node
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=self._get_empty_values(),
                                                  tags=("subcategory",))
                
                # Filter data for this subcategory
                subcategory_data = category_data[category_data['Subcategory'] == subcategory_name]
                
                sub_subcategories = sub.get('sub_subcategories', [])
                for subsub in sub_subcategories:
                    sub_subcategory_name = subsub.get('name', '')
                    if not sub_subcategory_name:
                        continue
                        
                    # Create sub-subcategory node
                    sub_subcategory_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sub_subcategory_name,
                                                   values=self._get_empty_values(),
                                                   tags=("sub_subcategory",))
                    
                    # Filter data for this sub-subcategory
                    # Note: JSON uses 'name' which maps to 'Sub-subcategory' in DataFrame
                    sub_subcategory_data = subcategory_data[subcategory_data['Sub-subcategory'] == sub_subcategory_name]
                    
                    # Add ERP Name items under sub-subcategory
                    erp_items = list(sub_subcategory_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        self._insert_erp_item(sub_subcategory_node, row, index)

    def _get_erp_name_full(self, row):
        """Extract full_name from ERP name object or return string value."""
        erp_name = row.get('ERP Name', '')
        if isinstance(erp_name, dict):
            return erp_name.get('full_name', '')
        elif pd.isna(erp_name):
            return ''
        else:
            return str(erp_name)
    
    def _insert_erp_item(self, parent_node, row, index, visible_columns=None):
        """Helper to insert an ERP item into the tree."""
        # Create row ID for this item
        sub_subcategory_value = row.get('Sub-subcategory', '')
        erp_name_full = self._get_erp_name_full(row)
        row_id = self._build_row_id(erp_name_full, row.get('Category', ''), row.get('Subcategory', ''), sub_subcategory_value)
        
        if visible_columns:
            # Use provided visible columns
            columns_to_use = visible_columns
        else:
            # Use all columns if not provided
            columns_to_use = self.tree["columns"]

        # Create values tuple
        values = []
        for col in columns_to_use:
            # Use mapping to get data column name
            data_col = self.get_data_column_name(col)
            if col == "ERP Name":
                # Extract full_name from ERP name object for display
                values.append(self._get_erp_name_full(row))
            else:
                values.append(row.get(data_col, ''))
        
        # Determine alternating background tag
        row_tag = "erp_item_even" if index % 2 == 0 else "erp_item_odd"
        
        # Create ERP item node with row ID and alternating color tag stored in tags
        self.tree.insert(parent_node, "end", 
                       text=erp_name_full,
                       values=tuple(values),
                       tags=(row_tag, row_id))
        
        # Expand all nodes by default
        self.expand_all()
        
    def expand_all(self):
        """Expand all tree nodes."""
        def expand_children(item):
            for child in self.tree.get_children(item):
                self.tree.item(child, open=True)
                expand_children(child)
        
        for item in self.tree.get_children():
            self.tree.item(item, open=True)
            expand_children(item)
    
    def _get_empty_values(self):
        """Get empty values tuple matching the number of columns."""
        columns = self.tree["columns"] if self.tree["columns"] else []
        return ("",) * len(columns)
            
    def get_data(self):
        """Get the current data from the tree view."""
        return self.data
        
    def has_data(self):
        """Check if the tree view has data."""
        return self.data is not None and not self.data.empty
        
    def get_all_columns(self):
        """Get all available columns (master list) from loaded data."""
        if self._all_columns:
            return self._all_columns
        # Fallback if no data loaded yet
        return tuple()
    
    def get_display_column_name(self, data_column):
        """Map data column name to display column name."""
        return data_column
    
    def get_visible_columns(self):
        """Get the currently visible columns."""
        if self.visible_columns:
            return self.visible_columns
        else:
            # Return all columns if no visibility settings
            return self.get_all_columns()
        
    def set_visible_columns(self, visible_columns):
        """Set the visible columns."""
        self.visible_columns = visible_columns
        
        # Save to config if config_manager is available
        if self.config_manager:
            self.config_manager.save_column_visibility(visible_columns)
        
        # Recreate tree view with only visible columns
        if visible_columns and self.data is not None:
            # Store current data
            current_data = self.data
            
            # Clear and recreate tree with new columns
            self.clear_tree()
            self.setup_columns_with_visibility(visible_columns)
            
            # Reload data with new column structure
            self.populate_tree_with_visibility(current_data, visible_columns)
            
            # Expand all nodes
            self.expand_all()
    
    def setup_columns_with_visibility(self, visible_columns):
        """Setup tree view columns with only visible columns."""
        # Use the visible columns as-is (respect user preferences)
        columns_to_use = visible_columns.copy() if visible_columns else []
        
        # Set only visible columns
        self.tree["columns"] = columns_to_use
        
        # Configure column headings
        self.tree.heading("#0", text="Hierarchy", anchor="w")
        for col in columns_to_use:
            self.tree.heading(col, text=col)
        
        # Configure column widths
        self.tree.column("#0", width=200, minwidth=150)
        for col in columns_to_use:
            if col == "User ERP Name":
                self.tree.column(col, width=150, minwidth=120)
            else:
                self.tree.column(col, width=100, minwidth=80)
    
    def populate_tree_with_visibility(self, data, visible_columns):
        """Populate the tree with only visible columns."""
        # Use the visible columns as-is (respect user preferences)
        columns_to_use = visible_columns.copy() if visible_columns else []
        
        if self.categories:
            # Use loaded categories to build the tree
            self._populate_tree_from_categories_with_visibility(data, self.categories, columns_to_use)
        else:
            # Fallback to grouping by data columns
            self._populate_tree_from_data_with_visibility(data, columns_to_use)

    def _populate_tree_from_data_with_visibility(self, data, columns_to_use):
        """Populate the tree by grouping data columns with visible columns."""
        if 'Category' not in data.columns:
            return
        
        # Group by Category
        categories = data.groupby('Category')
        
        for category_name, category_data in categories:
            # Create category node with color tag
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=("",) * len(columns_to_use),
                                           tags=("category",))
            
            # Group by Subcategory within category
            subcategories = category_data.groupby('Subcategory')
            
            for subcategory_name, subcategory_data in subcategories:
                # Create subcategory node with color tag
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=("",) * len(columns_to_use),
                                                  tags=("subcategory",))
                
                # Group by Sub-subcategory within subcategory
                sub_subcategories = subcategory_data.groupby('Sub-subcategory')
                
                for sub_subcategory_name, sub_subcategory_data in sub_subcategories:
                    # Create sub-subcategory node with color tag
                    sub_subcategory_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sub_subcategory_name,
                                                   values=("",) * len(columns_to_use),
                                                   tags=("sub_subcategory",))
                    
                    # Add ERP Name items under sub-subcategory with alternating backgrounds
                    erp_items = list(sub_subcategory_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        self._insert_erp_item(sub_subcategory_node, row, index, columns_to_use)

    def _populate_tree_from_categories_with_visibility(self, data, categories, columns_to_use):
        """Populate the tree using the categories structure with visible columns."""
        for category in categories:
            category_name = category.get('category', '')
            if not category_name:
                continue
                
            # Create category node
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=("",) * len(columns_to_use),
                                           tags=("category",))
            
            # Filter data for this category
            category_data = data[data['Category'] == category_name]
            
            subcategories = category.get('subcategories', [])
            for sub in subcategories:
                subcategory_name = sub.get('name', '')
                if not subcategory_name:
                    continue
                    
                # Create subcategory node
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=("",) * len(columns_to_use),
                                                  tags=("subcategory",))
                
                # Filter data for this subcategory
                subcategory_data = category_data[category_data['Subcategory'] == subcategory_name]
                
                sub_subcategories = sub.get('sub_subcategories', [])
                for subsub in sub_subcategories:
                    sub_subcategory_name = subsub.get('name', '')
                    if not sub_subcategory_name:
                        continue
                        
                    # Create sub-subcategory node
                    sub_subcategory_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sub_subcategory_name,
                                                   values=("",) * len(columns_to_use),
                                                   tags=("sub_subcategory",))
                    
                    # Filter data for this sub-subcategory
                    sub_subcategory_data = subcategory_data[subcategory_data['Sub-subcategory'] == sub_subcategory_name]
                    
                    # Add ERP Name items under sub-subcategory
                    erp_items = list(sub_subcategory_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        self._insert_erp_item(sub_subcategory_node, row, index, columns_to_use)
    
    def load_column_visibility(self, config_manager):
        """Load column visibility settings from config manager."""
        visible_columns = config_manager.get_column_visibility()
        if visible_columns:
            self.set_visible_columns(visible_columns)
    
    def apply_filter(self, column, filter_value, filter_type="contains"):
        """Apply a filter to a specific column."""
        self.active_filters[column] = {
            'value': filter_value,
            'type': filter_type
        }
        self._invalidate_filtered_cache()
        self.refresh_view()
    
    def remove_filter(self, column):
        """Remove filter from a specific column."""
        if column in self.active_filters:
            del self.active_filters[column]
            self._invalidate_filtered_cache()
            self.refresh_view()
    
    def clear_all_filters(self):
        """Clear all active filters."""
        self.active_filters.clear()
        self._invalidate_filtered_cache()
        self.refresh_view()
    
    def get_filtered_data(self):
        """Get data with active filters applied."""
        if self.data is None or self.data.empty:
            return pd.DataFrame(columns=self._all_columns)

        filters_signature = tuple(sorted((col, info['value'], info['type']) for col, info in self.active_filters.items()))
        cache = self._filtered_cache
        if cache and cache['version'] == self._mod_version and cache['filters'] == filters_signature and cache['base_id'] == self._base_data_id:
            return cache['data']

        filtered_data = self.get_data_with_modifications()
        if filtered_data is None:
            filtered_data = pd.DataFrame(columns=self._all_columns)
        else:
            for column, filter_info in self.active_filters.items():
                filter_value = filter_info['value']
                filter_type = filter_info['type']
                
                data_column = self.get_data_column_name(column)
                if data_column not in filtered_data.columns:
                    continue
                
                series = filtered_data[data_column].astype(str)
                if filter_type == "contains":
                    mask = series.str.contains(str(filter_value), case=False, na=False)
                elif filter_type == "equals":
                    mask = series == str(filter_value)
                elif filter_type == "starts_with":
                    mask = series.str.startswith(str(filter_value), na=False)
                elif filter_type == "ends_with":
                    mask = series.str.endswith(str(filter_value), na=False)
                else:
                    continue
                filtered_data = filtered_data[mask]

        self._filtered_cache = {
            'version': self._mod_version,
            'filters': filters_signature,
            'base_id': self._base_data_id,
            'data': filtered_data
        }

        return filtered_data
    
    def get_data_with_modifications(self):
        """Get data with user modifications applied."""
        if self.data is None or self.data.empty:
            return None

        if not self.user_modifications:
            return self.data

        cache = self._modified_cache
        if cache and cache['version'] == self._mod_version and cache['base_id'] == self._base_data_id:
            return cache['data']

        data = self.data.copy()

        def get_erp_full_name(erp_obj):
            if isinstance(erp_obj, dict):
                return erp_obj.get('full_name', '')
            elif pd.isna(erp_obj):
                return ''
            else:
                return str(erp_obj)

        erp_name_series = data['ERP Name'].apply(get_erp_full_name)

        for row_id, mods in self.user_modifications.items():
            base_row_id = mods.get('_base_row_id', row_id)
            erp_name, category, subcategory, sub_subcategory = self._parse_row_id(base_row_id)
            if not erp_name:
                continue
            mask = (
                (erp_name_series == erp_name) &
                (data['Category'] == category) &
                (data['Subcategory'] == subcategory) &
                (data['Sub-subcategory'] == sub_subcategory)
            )
            if not mask.any():
                continue

            if 'new_category' in mods and 'new_subcategory' in mods and 'new_sub_subcategory' in mods:
                data.loc[mask, 'Category'] = mods['new_category']
                data.loc[mask, 'Subcategory'] = mods['new_subcategory']
                data.loc[mask, 'Sub-subcategory'] = mods['new_sub_subcategory']
            if 'erp_name' in mods and mods['erp_name']:
                data.loc[mask, 'ERP Name'] = mods['erp_name']
            if 'manufacturer' in mods:
                data.loc[mask, 'Manufacturer'] = mods['manufacturer']
            if 'remark' in mods:
                data.loc[mask, 'Remark'] = mods['remark']
            if 'image' in mods:
                data.loc[mask, 'Image'] = mods['image']

        self._modified_cache = {
            'version': self._mod_version,
            'base_id': self._base_data_id,
            'data': data
        }

        return data
    
    def get_data_column_name(self, display_column):
        """Map display column names to data column names."""
        return display_column
    
    def refresh_view(self):
        """Refresh the tree view with current filters and visibility settings."""
        if self.data is not None and not self.data.empty:
            # Get filtered data
            self.filtered_data = self.get_filtered_data()
            
            # Clear current view
            self.clear_tree()
            
            # Apply column visibility settings if they exist
            if self.visible_columns:
                self.setup_columns_with_visibility(self.visible_columns)
                self.populate_tree_with_visibility(self.filtered_data, self.visible_columns)
            else:
                # Group data by hierarchy with all columns
                self.populate_tree(self.filtered_data)
            
            # Expand all nodes
            self.expand_all()
        else:
            self.clear_tree()
            if self.visible_columns:
                self.setup_columns_with_visibility(self.visible_columns)
                self.populate_tree_with_visibility(pd.DataFrame(columns=self._all_columns), self.visible_columns)
            else:
                self.populate_tree(pd.DataFrame(columns=self._all_columns))

    # ------------------------------------------------------------------
    # Added items support
    # ------------------------------------------------------------------
    def set_added_data(self, data: pd.DataFrame) -> None:
        """Store the draft dataset for quick toggling."""
        if data is None:
            self.added_data = pd.DataFrame(columns=self.primary_columns)
        else:
            self.added_data = data.copy(deep=True)

    def show_added_items(self) -> None:
        """Switch the tree view to the draft dataset."""
        if self.added_data is not None and not self.added_data.empty:
            dataset = self.added_data
        else:
            columns = self.primary_columns if self.primary_columns else self.get_all_columns()
            dataset = pd.DataFrame(columns=columns)
        self.load_data(dataset, self.categories, set_primary=False)
        self.current_view = "added"

    def show_primary_items(self) -> None:
        """Return the tree view to the main dataset."""
        if self.primary_data is not None:
            dataset = self.primary_data
        else:
            dataset = pd.DataFrame(columns=self.primary_columns)
        self.load_data(dataset, self.categories, set_primary=False)
        self.current_view = "primary"

    def is_showing_added_items(self) -> bool:
        """Whether the tree view currently displays draft items."""
        return self.current_view == "added"
    
    def get_unique_values(self, column):
        """Get unique values for a specific column for filter options."""
        if self.data is None or self.data.empty:
            return []
        
        data_column = self.get_data_column_name(column)
        if data_column not in self.data.columns:
            return []
        
        unique_values = self.data[data_column].dropna().unique()
        return sorted([str(val) for val in unique_values if val != ''])
    
    def get_current_filters(self):
        """Get current active filters."""
        return self.active_filters.copy()
    
    def load_filters(self, filters):
        """Load saved filters."""
        self.active_filters = filters.copy()
        if self.active_filters:
            self.refresh_view()
    
    def get_selected_item_data(self):
        """Get data for the currently selected item."""
        return self.selected_item
    
    def set_selected_item(self, item_data):
        """Set the selected item data."""
        self.selected_item = item_data
    
    def update_user_erp_name(self, row_id, erp_name):
        """Update ERP name for a specific row."""
        entry = self._ensure_mod_entry(row_id)
        entry['erp_name'] = erp_name
        self.update_tree_item_erp_name(row_id, erp_name)
        self._mark_data_dirty()
    
    def update_manufacturer(self, row_id, manufacturer):
        """Update manufacturer for a specific row."""
        entry = self._ensure_mod_entry(row_id)
        entry['manufacturer'] = manufacturer
        # Note: Manufacturer updates will be reflected in tree view when data is refreshed
        self._mark_data_dirty()
    
    def update_remark(self, row_id, remark):
        """Update remark for a specific row."""
        entry = self._ensure_mod_entry(row_id)
        entry['remark'] = remark
        # Note: Remark updates will be reflected in tree view when data is refreshed
        self._mark_data_dirty()
    
    def reassign_item(self, row_id, new_category, new_subcategory, new_sub_subcategory):
        """Reassign an item to a new category, subcategory, and sub_subcategory."""
        entry = self._ensure_mod_entry(row_id)
        entry['new_category'] = new_category
        entry['new_subcategory'] = new_subcategory
        entry['new_sub_subcategory'] = new_sub_subcategory

        base_row_id = entry.get('_base_row_id', row_id)
        base_erp, _, _, _ = self._parse_row_id(base_row_id)
        new_row_id = self._build_row_id(base_erp, new_category, new_subcategory, new_sub_subcategory)

        if new_row_id != row_id:
            self.user_modifications[new_row_id] = entry
            del self.user_modifications[row_id]

        self._mark_data_dirty()
        self.refresh_view()
        return new_row_id
    
    def update_tree_item_erp_name(self, row_id, erp_name):
        """Update the ERP name (tree item text) for a specific tree item without refreshing the entire view."""
        # Extract full_name from object if it's a dict
        if isinstance(erp_name, dict):
            display_name = erp_name.get('full_name', '')
        else:
            display_name = str(erp_name) if erp_name else ''
        
        # Find the tree item with the matching row_id
        for item in self.tree.get_children():
            # Check ERP items recursively
            if self._update_item_erp_name_recursive(item, row_id, display_name):
                break
    
    def _update_item_erp_name_recursive(self, item, row_id, display_name):
        """Recursively search for and update the ERP name (tree item text) for a specific item."""
        # Check if this item has the matching row_id
        tags = self.tree.item(item, "tags")
        if tags and len(tags) >= 2 and tags[1] == row_id:
            # Found the item, update its text (which displays ERP name full_name)
            self.tree.item(item, text=display_name)
            return True
        
        # Check children recursively
        for child in self.tree.get_children(item):
            if self._update_item_erp_name_recursive(child, row_id, display_name):
                return True
        
        return False
    
    def get_user_modifications(self):
        """Get all user modifications."""
        return self.user_modifications.copy()
    
    def get_unique_categories(self):
        """Get unique categories from data or loaded categories structure."""
        if self.categories:
            return sorted([cat.get('category', '') for cat in self.categories if cat.get('category')])
            
        if self.data is None or self.data.empty:
            return []
        return sorted(self.data['Category'].dropna().unique().tolist())
    
    def get_unique_subcategories(self, category=None):
        """Get unique subcategories from data or loaded categories structure."""
        if self.categories:
            subcategories = []
            for cat in self.categories:
                if not category or cat.get('category') == category:
                    for sub in cat.get('subcategories', []):
                        name = sub.get('name')
                        if name:
                            subcategories.append(name)
            return sorted(list(set(subcategories)))
            
        if self.data is None or self.data.empty:
            return []
        if category:
            filtered_data = self.data[self.data['Category'] == category]
            return sorted(filtered_data['Subcategory'].dropna().unique().tolist())
        return sorted(self.data['Subcategory'].dropna().unique().tolist())
    
    def get_unique_sub_subcategories(self, category=None, subcategory=None):
        """Get unique sub_subcategories from data or loaded categories structure."""
        if self.categories:
            sub_subcategories = []
            for cat in self.categories:
                if not category or cat.get('category') == category:
                    for sub in cat.get('subcategories', []):
                        if not subcategory or sub.get('name') == subcategory:
                            for subsub in sub.get('sub_subcategories', []):
                                name = subsub.get('name')
                                if name:
                                    sub_subcategories.append(name)
            return sorted(list(set(sub_subcategories)))
            
        if self.data is None or self.data.empty:
            return []
        filtered_data = self.data
        if category:
            filtered_data = filtered_data[filtered_data['Category'] == category]
        if subcategory:
            filtered_data = filtered_data[filtered_data['Subcategory'] == subcategory]
        
        # Use the Sub-subcategorycolumn with trailing space
        sub_subcategory_col = 'Sub-subcategory'
        return sorted(filtered_data[sub_subcategory_col].dropna().unique().tolist())
    
    def on_mouse_motion(self, event):
        """Handle mouse motion for hover effects."""
        item = self.tree.identify_row(event.y)
        if item:
            # Remove hover from all items
            for child in self.tree.get_children():
                self.tree.item(child, tags=self.tree.item(child, "tags")[:-1] if self.tree.item(child, "tags") and self.tree.item(child, "tags")[-1] == "hover" else self.tree.item(child, "tags"))
                self.remove_hover_recursive(child)
            
            # Add hover to current item
            current_tags = self.tree.item(item, "tags")
            if current_tags and "hover" not in current_tags:
                self.tree.item(item, tags=current_tags + ("hover",))
    
    def remove_hover_recursive(self, item):
        """Recursively remove hover tags from item and its children."""
        current_tags = self.tree.item(item, "tags")
        if current_tags and "hover" in current_tags:
            new_tags = [tag for tag in current_tags if tag != "hover"]
            self.tree.item(item, tags=new_tags)
        
        for child in self.tree.get_children(item):
            self.remove_hover_recursive(child)
    
    def on_mouse_leave(self, event):
        """Handle mouse leave to remove hover effects."""
        # Remove hover from all items
        for child in self.tree.get_children():
            self.tree.item(child, tags=self.tree.item(child, "tags")[:-1] if self.tree.item(child, "tags") and self.tree.item(child, "tags")[-1] == "hover" else self.tree.item(child, "tags"))
            self.remove_hover_recursive(child)
    
    def delete_item(self, row_id):
        """Delete an item from the tree view and data."""
        if not self.data is not None or self.data.empty:
            return
            
        # Find and remove the item from the tree
        for item in self.tree.get_children():
            if self._delete_item_recursive(item, row_id):
                break
                
        # Remove from user modifications if exists
        if row_id in self.user_modifications:
            del self.user_modifications[row_id]
            
        # Remove from data
        if self.data is not None and not self.data.empty:
            # Find the row index by matching the row_id components
            base_row_id = self._get_base_row_id(row_id)
            erp_name, category, subcategory, sub_subcategory = self._parse_row_id(base_row_id)
            if erp_name:
                
                # Create mask to find the row to delete - extract full_name from ERP name object
                def get_erp_full_name(erp_obj):
                    if isinstance(erp_obj, dict):
                        return erp_obj.get('full_name', '')
                    elif pd.isna(erp_obj):
                        return ''
                    else:
                        return str(erp_obj)
                
                erp_name_series = self.data['ERP Name'].apply(get_erp_full_name)
                mask = (
                    (erp_name_series == erp_name) &
                    (self.data['Category'] == category) &
                    (self.data['Subcategory'] == subcategory) &
                    (self.data['Sub-subcategory'] == sub_subcategory)
                )
                
                # Remove the row
                self.data = self.data[~mask]
                self._base_data_id = id(self.data)
                self._mark_data_dirty()
                
                # Refresh the view
                self.refresh_view()
    
    def _delete_item_recursive(self, item, row_id):
        """Recursively search for and delete an item with the given row_id."""
        # Check if this item has the matching row_id
        item_tags = self.tree.item(item, "tags")
        if item_tags and "erp_item" in str(item_tags):
            # This is an ERP item, check if it matches
            item_values = self.tree.item(item, "values")
            if item_values and len(item_values) > 0:
                # Get the ERP name from the values (assuming it's in the ERP Name column)
                erp_name = item_values[1] if len(item_values) > 1 else ""  # ERP Name is typically the second column
                
                # Check if this matches our row_id
                delimiter = self.ROW_ID_DELIMITER
                if row_id.startswith(erp_name + delimiter):
                    # Found the item, delete it
                    self.tree.delete(item)
                    return True
        
        # Check children recursively
        for child in self.tree.get_children(item):
            if self._delete_item_recursive(child, row_id):
                return True
                
        return False
