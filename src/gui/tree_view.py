"""
Tree View Widget for ERP Database Editor
Displays data in hierarchical tree format with Article Category, Subcategory, and Sublevel.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import pandas as pd


class TreeViewWidget(ctk.CTkFrame):
    """Tree view widget for displaying hierarchical ERP data."""
    
    def __init__(self, parent):
        """Initialize the tree view widget."""
        super().__init__(parent)
        
        # Data storage
        self.data = None
        self.visible_columns = None
        self.filtered_data = None
        self.active_filters = {}
        
        # User modifications tracking
        self.user_modifications = {}
        self.selected_item = None
        self.selected_items = []  # For multi-selection support
        
        # Create the tree view
        self.create_tree_view()
        
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
    
    def configure_tree_style(self):
        """Configure the tree view styling with dark mode colors and fonts."""
        # Create a style object
        style = ttk.Style()
        
        # Configure the treeview style with dark theme
        style.configure("Treeview", 
                       font=("Arial", 9),  # Smaller font size
                       rowheight=20,  # Smaller row height
                       background="#2b2b2b",  # Dark background
                       foreground="#ffffff",  # White text
                       fieldbackground="#2b2b2b")  # Dark field background
        
        # Configure treeview heading with dark theme
        style.configure("Treeview.Heading",
                       font=("Arial", 9, "bold"),  # Bold headers with smaller font
                       background="#3c3c3c",  # Darker header background
                       foreground="#ffffff")  # White header text
        
        # Define dark color schemes for different hierarchy levels
        self.hierarchy_colors = {
            'category': '#404040',      # Dark gray for categories
            'subcategory': '#4a4a4a',   # Slightly lighter gray for subcategories  
            'sublevel': '#545454',      # Even lighter gray for sublevels
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
        
        self.tree.tag_configure('sublevel',
                               background=self.hierarchy_colors['sublevel'],
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
        # Define the hierarchy columns
        self.tree["columns"] = ("User ERP Name", "ERP Name", "CAD Name", "Electronics", "Product Value", 
                              "Manufacturer", "SKU", "EAN 13", "Unit", "Supplier", 
                              "Expiry Date", "Tracking Method", "Procurement Method", "Remark")
        
        # Configure column headings
        self.tree.heading("#0", text="Hierarchy", anchor="w")
        self.tree.heading("User ERP Name", text="User ERP Name")
        self.tree.heading("ERP Name", text="ERP Name")
        self.tree.heading("CAD Name", text="CAD Name")
        self.tree.heading("Electronics", text="Electronics")
        self.tree.heading("Product Value", text="Product Value")
        self.tree.heading("Manufacturer", text="Manufacturer")
        self.tree.heading("SKU", text="SKU")
        self.tree.heading("EAN 13", text="EAN 13")
        self.tree.heading("Unit", text="Unit")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.heading("Expiry Date", text="Expiry Date")
        self.tree.heading("Tracking Method", text="Tracking Method")
        self.tree.heading("Procurement Method", text="Procurement Method")
        self.tree.heading("Remark", text="Remark")
        
        # Configure column widths
        self.tree.column("#0", width=200, minwidth=150)
        self.tree.column("User ERP Name", width=150, minwidth=120)
        for col in self.tree["columns"][1:]:  # Skip User ERP Name as it's already configured
            self.tree.column(col, width=100, minwidth=80)
            
    def load_data(self, data):
        """Load data into the tree view."""
        self.data = data
        # Clear filters when loading new data
        self.active_filters.clear()
        self.refresh_view()
            
    def clear_tree(self):
        """Clear all items from the tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def populate_tree(self, data):
        """Populate the tree with hierarchical data."""
        # Group by Article Category
        categories = data.groupby('Article Category')
        
        for category_name, category_data in categories:
            # Create category node with color tag
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=("", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                           tags=("category",))
            
            # Group by Article Subcategory within category
            subcategories = category_data.groupby('Article Subcategory')
            
            for subcategory_name, subcategory_data in subcategories:
                # Create subcategory node with color tag
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=("", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                                  tags=("subcategory",))
                
                # Group by Article Sublevel within subcategory
                sublevels = subcategory_data.groupby('Article Sublevel ')
                
                for sublevel_name, sublevel_data in sublevels:
                    # Create sublevel node with color tag
                    sublevel_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sublevel_name,
                                                   values=("", "", "", "", "", "", "", "", "", "", "", "", "", ""),
                                                   tags=("sublevel",))
                    
                    # Add ERP Name items under sublevel with alternating backgrounds
                    erp_items = list(sublevel_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        # Create row ID for this item (use the Article Sublevel column with trailing space)
                        sublevel = row.get('Article Sublevel ', '')
                        # Use a unique delimiter that's unlikely to appear in the data
                        delimiter = "◆◆◆"  # Using a unique Unicode character sequence
                        row_id = f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{sublevel}"
                        
                        erp_name = row.get('ERP name', '')
                        cad_name = row.get('CAD name', '')
                        electronics = row.get('Electronics', '')
                        product_value = row.get('Product Value', '')
                        manufacturer = row.get('Manufacturer', '')
                        sku = row.get('SKU', '')
                        ean13 = row.get('EAN 13', '')
                        unit = row.get('Unit', '')
                        supplier = row.get('Supplier', '')
                        expiry_date = row.get('Expiry Date (Y/N)', '')
                        tracking_method = row.get('Tracking Method', '')
                        procurement_method = row.get('Procurement Method (Buy/Make)', '')
                        remark = row.get('REMARK', '')
                        
                        # Get user ERP name - first check if it exists in original data, then check modifications
                        user_erp_name = row.get('User ERP Name', '')
                        if row_id in self.user_modifications and 'user_erp_name' in self.user_modifications[row_id]:
                            user_erp_name = self.user_modifications[row_id]['user_erp_name']
                        
                        # Determine alternating background tag
                        row_tag = "erp_item_even" if index % 2 == 0 else "erp_item_odd"
                        
                        # Create ERP item node with row ID and alternating color tag stored in tags
                        self.tree.insert(sublevel_node, "end", 
                                       text=erp_name,
                                       values=(user_erp_name, erp_name, cad_name, electronics, product_value,
                                              manufacturer, sku, ean13, unit, supplier,
                                              expiry_date, tracking_method, procurement_method, remark),
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
            
    def get_data(self):
        """Get the current data from the tree view."""
        return self.data
        
    def has_data(self):
        """Check if the tree view has data."""
        return self.data is not None and not self.data.empty
        
    def get_visible_columns(self):
        """Get the currently visible columns."""
        if self.visible_columns:
            return self.visible_columns
        else:
            # Return all columns if no visibility settings
            return self.tree["columns"]
        
    def set_visible_columns(self, visible_columns):
        """Set the visible columns."""
        self.visible_columns = visible_columns
        
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
        # Create a copy to avoid modifying the original list
        columns_to_use = visible_columns.copy()
        
        # Add User ERP Name column if it's not in visible columns
        if "User ERP Name" not in columns_to_use:
            columns_to_use = ["User ERP Name"] + columns_to_use
        
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
        # Create a copy to avoid modifying the original list
        columns_to_use = visible_columns.copy()
        
        # Add User ERP Name column if it's not in visible columns
        if "User ERP Name" not in columns_to_use:
            columns_to_use = ["User ERP Name"] + columns_to_use
        
        # Group by Article Category
        categories = data.groupby('Article Category')
        
        for category_name, category_data in categories:
            # Create category node with color tag
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=("",) * len(columns_to_use),
                                           tags=("category",))
            
            # Group by Article Subcategory within category
            subcategories = category_data.groupby('Article Subcategory')
            
            for subcategory_name, subcategory_data in subcategories:
                # Create subcategory node with color tag
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=("",) * len(columns_to_use),
                                                  tags=("subcategory",))
                
                # Group by Article Sublevel within subcategory
                sublevels = subcategory_data.groupby('Article Sublevel ')
                
                for sublevel_name, sublevel_data in sublevels:
                    # Create sublevel node with color tag
                    sublevel_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sublevel_name,
                                                   values=("",) * len(columns_to_use),
                                                   tags=("sublevel",))
                    
                    # Add ERP Name items under sublevel with alternating backgrounds
                    erp_items = list(sublevel_data.iterrows())
                    for index, (_, row) in enumerate(erp_items):
                        # Create values tuple with only visible columns
                        values = []
                        for col in columns_to_use:
                            if col == "User ERP Name":
                                # Get user ERP name - first check if it exists in original data, then check modifications
                                sublevel = row.get('Article Sublevel', '')
                                # Use a unique delimiter that's unlikely to appear in the data
                                delimiter = "◆◆◆"  # Using a unique Unicode character sequence
                                row_id = f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{sublevel}"
                                user_value = row.get('User ERP Name', '')
                                if row_id in self.user_modifications and 'user_erp_name' in self.user_modifications[row_id]:
                                    user_value = self.user_modifications[row_id]['user_erp_name']
                                values.append(user_value)
                            elif col == "ERP Name":
                                values.append(row.get('ERP name', ''))
                            elif col == "CAD Name":
                                values.append(row.get('CAD name', ''))
                            elif col == "Electronics":
                                values.append(row.get('Electronics', ''))
                            elif col == "Product Value":
                                values.append(row.get('Product Value', ''))
                            elif col == "Manufacturer":
                                values.append(row.get('Manufacturer', ''))
                            elif col == "SKU":
                                values.append(row.get('SKU', ''))
                            elif col == "EAN 13":
                                values.append(row.get('EAN 13', ''))
                            elif col == "Unit":
                                values.append(row.get('Unit', ''))
                            elif col == "Supplier":
                                values.append(row.get('Supplier', ''))
                            elif col == "Expiry Date":
                                values.append(row.get('Expiry Date (Y/N)', ''))
                            elif col == "Tracking Method":
                                values.append(row.get('Tracking Method', ''))
                            elif col == "Procurement Method":
                                values.append(row.get('Procurement Method (Buy/Make)', ''))
                            elif col == "Remark":
                                values.append(row.get('REMARK', ''))
                            else:
                                values.append('')
                        
                        # Create row ID for this item (use the Article Sublevel column with trailing space)
                        sublevel = row.get('Article Sublevel ', '')
                        # Use a unique delimiter that's unlikely to appear in the data
                        delimiter = "◆◆◆"  # Using a unique Unicode character sequence
                        row_id = f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{sublevel}"
                        
                        # Determine alternating background tag
                        row_tag = "erp_item_even" if index % 2 == 0 else "erp_item_odd"
                        
                        # Create ERP item node with row ID and alternating color tag stored in tags
                        item = self.tree.insert(sublevel_node, "end", 
                                               text=row.get('ERP name', ''),
                                               values=tuple(values),
                                               tags=(row_tag, row_id))
    
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
        self.refresh_view()
    
    def remove_filter(self, column):
        """Remove filter from a specific column."""
        if column in self.active_filters:
            del self.active_filters[column]
            self.refresh_view()
    
    def clear_all_filters(self):
        """Clear all active filters."""
        self.active_filters.clear()
        self.refresh_view()
    
    def get_filtered_data(self):
        """Get data with active filters applied."""
        if not self.data is not None or self.data.empty:
            return None
        
        filtered_data = self.data.copy()
        
        for column, filter_info in self.active_filters.items():
            filter_value = filter_info['value']
            filter_type = filter_info['type']
            
            # Map display column names to data column names
            data_column = self.get_data_column_name(column)
            if data_column not in filtered_data.columns:
                continue
            
            if filter_type == "contains":
                filtered_data = filtered_data[filtered_data[data_column].astype(str).str.contains(str(filter_value), case=False, na=False)]
            elif filter_type == "equals":
                filtered_data = filtered_data[filtered_data[data_column].astype(str) == str(filter_value)]
            elif filter_type == "starts_with":
                filtered_data = filtered_data[filtered_data[data_column].astype(str).str.startswith(str(filter_value), na=False)]
            elif filter_type == "ends_with":
                filtered_data = filtered_data[filtered_data[data_column].astype(str).str.endswith(str(filter_value), na=False)]
        
        return filtered_data
    
    def get_data_column_name(self, display_column):
        """Map display column names to data column names."""
        column_mapping = {
            "User ERP Name": "User ERP Name",  # This is a virtual column
            "ERP Name": "ERP name",
            "CAD Name": "CAD name",
            "Electronics": "Electronics",
            "Product Value": "Product Value",
            "Manufacturer": "Manufacturer",
            "SKU": "SKU",
            "EAN 13": "EAN 13",
            "Unit": "Unit",
            "Supplier": "Supplier",
            "Expiry Date": "Expiry Date (Y/N)",
            "Tracking Method": "Tracking Method",
            "Procurement Method": "Procurement Method (Buy/Make)",
            "Remark": "REMARK"
        }
        return column_mapping.get(display_column, display_column)
    
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
    
    def update_user_erp_name(self, row_id, user_erp_name):
        """Update user ERP name for a specific row."""
        if row_id not in self.user_modifications:
            self.user_modifications[row_id] = {}
        self.user_modifications[row_id]['user_erp_name'] = user_erp_name
        self.refresh_view()
    
    def reassign_item(self, row_id, new_category, new_subcategory, new_sublevel):
        """Reassign an item to a new category, subcategory, and sublevel."""
        if row_id not in self.user_modifications:
            self.user_modifications[row_id] = {}
        self.user_modifications[row_id]['new_category'] = new_category
        self.user_modifications[row_id]['new_subcategory'] = new_subcategory
        self.user_modifications[row_id]['new_sublevel'] = new_sublevel
        self.refresh_view()
    
    def get_user_modifications(self):
        """Get all user modifications."""
        return self.user_modifications.copy()
    
    def get_unique_categories(self):
        """Get unique categories from data."""
        if self.data is None or self.data.empty:
            return []
        return sorted(self.data['Article Category'].dropna().unique().tolist())
    
    def get_unique_subcategories(self, category=None):
        """Get unique subcategories from data."""
        if self.data is None or self.data.empty:
            return []
        if category:
            filtered_data = self.data[self.data['Article Category'] == category]
            return sorted(filtered_data['Article Subcategory'].dropna().unique().tolist())
        return sorted(self.data['Article Subcategory'].dropna().unique().tolist())
    
    def get_unique_sublevels(self, category=None, subcategory=None):
        """Get unique sublevels from data."""
        if self.data is None or self.data.empty:
            return []
        filtered_data = self.data
        if category:
            filtered_data = filtered_data[filtered_data['Article Category'] == category]
        if subcategory:
            filtered_data = filtered_data[filtered_data['Article Subcategory'] == subcategory]
        
        # Use the Article Sublevel column with trailing space
        sublevel_col = 'Article Sublevel '
        return sorted(filtered_data[sublevel_col].dropna().unique().tolist())
    
    def clear_user_erp_names_for_selected(self):
        """Clear User ERP Name for all selected items."""
        if not self.selected_items:
            return 0
            
        cleared_count = 0
        for item_data, row_id in self.selected_items:
            if row_id in self.user_modifications:
                if 'user_erp_name' in self.user_modifications[row_id]:
                    del self.user_modifications[row_id]['user_erp_name']
                    cleared_count += 1
            else:
                # Add empty user_erp_name to track that it was explicitly cleared
                self.user_modifications[row_id] = {'user_erp_name': ''}
                cleared_count += 1
        
        # Refresh the tree view to show changes
        if cleared_count > 0:
            self.refresh_view()
        
        return cleared_count
    
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
