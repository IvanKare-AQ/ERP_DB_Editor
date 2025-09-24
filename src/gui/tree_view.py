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
        
        # Create the tree view
        self.create_tree_view()
        
    def create_tree_view(self):
        """Create the tree view component."""
        # Create frame for tree view and scrollbars
        self.tree_frame = ctk.CTkFrame(self)
        self.tree_frame.pack(fill="both", expand=True)
        
        # Create tree view
        self.tree = ttk.Treeview(self.tree_frame)
        
        # Create scrollbars
        self.v_scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.h_scrollbar = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        
        # Configure tree view
        self.tree.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        
        # Pack components
        self.tree.pack(side="left", fill="both", expand=True)
        self.v_scrollbar.pack(side="right", fill="y")
        self.h_scrollbar.pack(side="bottom", fill="x")
        
        # Configure columns
        self.setup_columns()
        
    def setup_columns(self):
        """Setup the tree view columns."""
        # Define the hierarchy columns
        self.tree["columns"] = ("ERP Name", "CAD Name", "Electronics", "Product Value", 
                              "Manufacturer", "SKU", "EAN 13", "Unit", "Supplier", 
                              "Expiry Date", "Tracking Method", "Procurement Method", "Remark")
        
        # Configure column headings
        self.tree.heading("#0", text="Hierarchy", anchor="w")
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
        for col in self.tree["columns"]:
            self.tree.column(col, width=100, minwidth=80)
            
    def load_data(self, data):
        """Load data into the tree view."""
        self.data = data
        self.clear_tree()
        
        if data is not None and not data.empty:
            # Group data by hierarchy
            self.populate_tree(data)
            
            # Apply column visibility settings if they exist
            if self.visible_columns:
                self.set_visible_columns(self.visible_columns)
            
    def clear_tree(self):
        """Clear all items from the tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
    def populate_tree(self, data):
        """Populate the tree with hierarchical data."""
        # Group by Article Category
        categories = data.groupby('Article Category')
        
        for category_name, category_data in categories:
            # Create category node
            category_node = self.tree.insert("", "end", text=category_name, 
                                           values=("", "", "", "", "", "", "", "", "", "", "", "", ""))
            
            # Group by Article Subcategory within category
            subcategories = category_data.groupby('Article Subcategory')
            
            for subcategory_name, subcategory_data in subcategories:
                # Create subcategory node
                subcategory_node = self.tree.insert(category_node, "end", 
                                                  text=subcategory_name,
                                                  values=("", "", "", "", "", "", "", "", "", "", "", "", ""))
                
                # Group by Article Sublevel within subcategory
                sublevels = subcategory_data.groupby('Article Sublevel')
                
                for sublevel_name, sublevel_data in sublevels:
                    # Create sublevel node
                    sublevel_node = self.tree.insert(subcategory_node, "end", 
                                                   text=sublevel_name,
                                                   values=("", "", "", "", "", "", "", "", "", "", "", "", ""))
                    
                    # Add ERP Name items under sublevel
                    for _, row in sublevel_data.iterrows():
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
                        
                        # Create ERP item node
                        self.tree.insert(sublevel_node, "end", 
                                       text=erp_name,
                                       values=(erp_name, cad_name, electronics, product_value,
                                              manufacturer, sku, ean13, unit, supplier,
                                              expiry_date, tracking_method, procurement_method, remark))
        
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
        
        # Hide/show columns based on visibility settings
        if visible_columns:
            # Get all available columns
            all_columns = self.tree["columns"]
            
            # Hide columns that are not in visible_columns
            for column in all_columns:
                if column not in visible_columns:
                    self.tree.column(column, width=0, minwidth=0)
                else:
                    # Restore column width if it was hidden
                    self.tree.column(column, width=100, minwidth=80)
            
            # Update the tree view to reflect changes
            self.tree.update()
    
    def load_column_visibility(self, config_manager):
        """Load column visibility settings from config manager."""
        visible_columns = config_manager.get_column_visibility()
        if visible_columns:
            self.set_visible_columns(visible_columns)
