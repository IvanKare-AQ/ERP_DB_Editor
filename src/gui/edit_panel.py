"""
Edit Panel for ERP Database Editor
Provides editing functionality for selected ERP items.
"""

import customtkinter as ctk
import tkinter as tk


class EditPanel(ctk.CTkFrame):
    """Panel for editing selected ERP items."""
    
    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the edit panel."""
        super().__init__(parent)
        
        self.tree_view = tree_view
        self.main_window = main_window
        self.selected_item = None
        self.selected_row_id = None
        
        # Configure panel size
        self.configure(width=350)
        
        # Create the edit panel
        self.setup_edit_panel()
        
    def setup_edit_panel(self):
        """Setup the edit panel components."""
        # Title
        title_label = ctk.CTkLabel(self, text="Edit Selected Item", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 20))
        
        # User ERP Name section
        self.setup_user_erp_name_section()
        
        # Separator
        separator1 = ctk.CTkFrame(self, height=2)
        separator1.pack(fill="x", padx=10, pady=20)
        
        # Reassignment section
        self.setup_reassignment_section()
        
    def setup_user_erp_name_section(self):
        """Setup the User ERP Name editing section."""
        # Section title
        section_title = ctk.CTkLabel(self, text="User ERP Name", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        section_title.pack(pady=(0, 10))
        
        # Input field
        self.user_erp_name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter User ERP Name...",
            width=300,
            height=35
        )
        self.user_erp_name_entry.pack(pady=(0, 10))
        
        # Update button
        self.update_name_button = ctk.CTkButton(
            self,
            text="Update Name",
            command=self.update_user_erp_name,
            width=120,
            height=35,
            state="disabled"
        )
        self.update_name_button.pack(pady=(0, 10))
        
    def setup_reassignment_section(self):
        """Setup the reassignment section."""
        # Section title
        section_title = ctk.CTkLabel(self, text="Reassign Item", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        section_title.pack(pady=(0, 10))
        
        # Category dropdown
        category_frame = ctk.CTkFrame(self)
        category_frame.pack(fill="x", padx=10, pady=5)
        
        category_label = ctk.CTkLabel(category_frame, text="Category:", width=100)
        category_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.category_dropdown = ctk.CTkOptionMenu(
            category_frame,
            values=["Select Category..."],
            command=self.on_category_change,
            width=200
        )
        self.category_dropdown.pack(side="left", padx=5, pady=10)
        
        # Subcategory dropdown
        subcategory_frame = ctk.CTkFrame(self)
        subcategory_frame.pack(fill="x", padx=10, pady=5)
        
        subcategory_label = ctk.CTkLabel(subcategory_frame, text="Subcategory:", width=100)
        subcategory_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.subcategory_dropdown = ctk.CTkOptionMenu(
            subcategory_frame,
            values=["Select Subcategory..."],
            command=self.on_subcategory_change,
            width=200
        )
        self.subcategory_dropdown.pack(side="left", padx=5, pady=10)
        
        # Sublevel dropdown
        sublevel_frame = ctk.CTkFrame(self)
        sublevel_frame.pack(fill="x", padx=10, pady=5)
        
        sublevel_label = ctk.CTkLabel(sublevel_frame, text="Sublevel:", width=100)
        sublevel_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.sublevel_dropdown = ctk.CTkOptionMenu(
            sublevel_frame,
            values=["Select Sublevel..."],
            width=200
        )
        self.sublevel_dropdown.pack(side="left", padx=5, pady=10)
        
        # Reassign button
        self.reassign_button = ctk.CTkButton(
            self,
            text="Reassign Item",
            command=self.reassign_item,
            width=120,
            height=35,
            state="disabled"
        )
        self.reassign_button.pack(pady=(20, 10))
        
    def load_categories(self):
        """Load categories into the dropdown."""
        categories = self.tree_view.get_unique_categories()
        if categories:
            self.category_dropdown.configure(values=["Select Category..."] + categories)
        else:
            self.category_dropdown.configure(values=["Select Category..."])
            
    def on_category_change(self, category):
        """Handle category selection change."""
        if category == "Select Category...":
            self.subcategory_dropdown.configure(values=["Select Subcategory..."])
            self.sublevel_dropdown.configure(values=["Select Sublevel..."])
            return
            
        # Load subcategories for selected category
        subcategories = self.tree_view.get_unique_subcategories(category)
        if subcategories:
            self.subcategory_dropdown.configure(values=["Select Subcategory..."] + subcategories)
        else:
            self.subcategory_dropdown.configure(values=["Select Subcategory..."])
        
        # Reset sublevel dropdown
        self.sublevel_dropdown.configure(values=["Select Sublevel..."])
        
    def on_subcategory_change(self, subcategory):
        """Handle subcategory selection change."""
        if subcategory == "Select Subcategory...":
            self.sublevel_dropdown.configure(values=["Select Sublevel..."])
            return
            
        category = self.category_dropdown.get()
        if category == "Select Category...":
            return
            
        # Load sublevels for selected category and subcategory
        sublevels = self.tree_view.get_unique_sublevels(category, subcategory)
        if sublevels:
            self.sublevel_dropdown.configure(values=["Select Sublevel..."] + sublevels)
        else:
            self.sublevel_dropdown.configure(values=["Select Sublevel..."])
            
    def set_selected_item(self, item_data, row_id):
        """Set the selected item and populate the edit fields."""
        self.selected_item = item_data
        self.selected_row_id = row_id
        
        
        if item_data:
            # Populate User ERP Name field with the original ERP name
            erp_name = item_data.get('ERP name', '')
            current_user_name = self.tree_view.user_modifications.get(row_id, {}).get('user_erp_name', '')
            # If no user name is set, use the original ERP name
            if not current_user_name:
                current_user_name = erp_name
            self.user_erp_name_entry.delete(0, tk.END)
            self.user_erp_name_entry.insert(0, current_user_name)
            
            # Set the dropdowns to current item's category/subcategory/sublevel
            current_category = item_data.get('Article Category', '')
            current_subcategory = item_data.get('Article Subcategory', '')
            current_sublevel = item_data.get('Article Sublevel', '')
            
            # Load categories first
            self.load_categories()
            
            # Set category dropdown
            if current_category:
                self.category_dropdown.set(current_category)
                # Load subcategories for this category
                subcategories = self.tree_view.get_unique_subcategories(current_category)
                if subcategories:
                    self.subcategory_dropdown.configure(values=["Select Subcategory..."] + subcategories)
                    if current_subcategory:
                        self.subcategory_dropdown.set(current_subcategory)
                        # Load sublevels for this category and subcategory
                        sublevels = self.tree_view.get_unique_sublevels(current_category, current_subcategory)
                        if sublevels:
                            self.sublevel_dropdown.configure(values=["Select Sublevel..."] + sublevels)
                            if current_sublevel:
                                self.sublevel_dropdown.set(current_sublevel)
            
            # Enable buttons
            self.update_name_button.configure(state="normal")
            self.reassign_button.configure(state="normal")
        else:
            # Clear fields and disable buttons
            self.user_erp_name_entry.delete(0, tk.END)
            self.user_erp_name_entry.insert(0, "")
            
            self.update_name_button.configure(state="disabled")
            self.reassign_button.configure(state="disabled")
            
            # Reset dropdowns
            self.category_dropdown.configure(values=["Select Category..."])
            self.subcategory_dropdown.configure(values=["Select Subcategory..."])
            self.sublevel_dropdown.configure(values=["Select Sublevel..."])
            
    def update_user_erp_name(self):
        """Update the user ERP name for the selected item."""
        if not self.selected_row_id:
            return
            
        user_erp_name = self.user_erp_name_entry.get().strip()
        self.tree_view.update_user_erp_name(self.selected_row_id, user_erp_name)
        
        # Update status if main window is available
        if self.main_window:
            if user_erp_name:
                self.main_window.update_status(f"Updated ERP name: {user_erp_name}")
            else:
                self.main_window.update_status("Cleared user ERP name")
        
    def reassign_item(self):
        """Reassign the selected item to new category, subcategory, and sublevel."""
        if not self.selected_row_id:
            return
            
        category = self.category_dropdown.get()
        subcategory = self.subcategory_dropdown.get()
        sublevel = self.sublevel_dropdown.get()
        
        if (category == "Select Category..." or 
            subcategory == "Select Subcategory..." or 
            sublevel == "Select Sublevel..."):
            return
            
        self.tree_view.reassign_item(self.selected_row_id, category, subcategory, sublevel)
        
        # Update status if main window is available
        if self.main_window:
            self.main_window.update_status(f"Reassigned item to: {category} > {subcategory} > {sublevel}")
