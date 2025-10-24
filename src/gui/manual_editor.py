"""
Manual Editor for ERP Database Editor
Provides manual editing functionality for selected ERP items.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class ManualEditor(ctk.CTkFrame):
    """Manual editor panel for editing selected ERP items."""

    # Width constants for consistent UI sizing
    INPUT_FIELD_WIDTH = 400      # Width for input fields (User ERP Name, Manufacturer, REMARK)
    FIELD_LABEL_WIDTH = 120      # Width for field labels (User ERP Name, Manufacturer, REMARK)
    DROPDOWN_LABEL_WIDTH = 100   # Width for dropdown labels (Category, Subcategory, Sublevel)
    DROPDOWN_WIDTH = 300         # Width for dropdown menus
    RESET_BUTTON_WIDTH = 60      # Width for reset buttons
    UPDATE_BUTTON_WIDTH = 120    # Width for update button
    DELETE_BUTTON_WIDTH = 150    # Width for delete button
    ACTION_BUTTON_WIDTH = 150    # Width for action buttons (Convert Multiline, Remove NEN)
    REASSIGN_BUTTON_WIDTH = 100  # Width for reassign button

    # Height constants for consistent UI sizing
    INPUT_FIELD_HEIGHT = 35      # Height for input fields
    BUTTON_HEIGHT = 35           # Unified height for all buttons
    REASSIGN_BUTTON_HEIGHT = 90  # Height for reassign button (spans multiple rows)
    SEPARATOR_HEIGHT = 2         # Height for separator lines
    IMAGE_PREVIEW_SIZE = 150     # Size for image preview (width and height in pixels)

    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the manual editor."""
        super().__init__(parent)

        self.tree_view = tree_view
        self.main_window = main_window
        self.selected_item = None
        self.selected_row_id = None
        
        # Image handling
        self.current_image_photo = None  # Store PhotoImage reference
        self.image_handler = None  # Will be initialized when Excel file is loaded

        # Panel will be sized by the tabview container

        # Create the manual editor interface
        self.setup_manual_editor()

    def setup_manual_editor(self):
        """Setup the manual editor components."""
        # Title
        title_label = ctk.CTkLabel(self, text="Manual Editing", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 5))
        
        # Small image preview centered
        image_container = ctk.CTkFrame(self, width=self.IMAGE_PREVIEW_SIZE, height=self.IMAGE_PREVIEW_SIZE)
        image_container.pack(pady=(0, 10))
        image_container.pack_propagate(False)  # Prevent resizing
        
        # Use tk.Label for image support
        self.image_preview_label = tk.Label(
            image_container,
            text="No Image",
            bg="#2b2b2b",  # Dark background
            fg="gray",
            relief="solid",
            borderwidth=1
        )
        self.image_preview_label.place(x=0, y=0, width=self.IMAGE_PREVIEW_SIZE, height=self.IMAGE_PREVIEW_SIZE)

        # User ERP Name section
        self.setup_user_erp_name_section(self)

        # Separator
        separator1 = ctk.CTkFrame(self, height=self.SEPARATOR_HEIGHT)
        separator1.pack(fill="x", padx=10, pady=10)

        # Reassignment section
        self.setup_reassignment_section(self)

        # Data cleaning section at the bottom
        self.setup_data_cleaning_section(self)

    def setup_user_erp_name_section(self, parent):
        """Setup the User ERP Name editing section."""
        # User ERP Name input field and buttons frame
        user_erp_frame = ctk.CTkFrame(parent)
        user_erp_frame.pack(anchor="w", pady=(0, 5))

        # User ERP Name label
        user_erp_label = ctk.CTkLabel(
            user_erp_frame,
            text="User ERP Name:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        user_erp_label.pack(side="left", padx=(10, 5))

        # User ERP Name input field
        self.user_erp_name_entry = ctk.CTkEntry(
            user_erp_frame,
            placeholder_text="Enter User ERP Name...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.user_erp_name_entry.pack(side="left", padx=(0, 10))
        # Bind to re-parse into Type, PN, Details when edited
        self.user_erp_name_entry.bind('<KeyRelease>', self.on_user_erp_name_change)

        # Reset button for User ERP Name
        self.reset_name_button = ctk.CTkButton(
            user_erp_frame,
            text="Reset",
            command=self.reset_user_erp_name,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            state="disabled"
        )
        self.reset_name_button.pack(side="left")

        # Manufacturer input field and buttons frame
        manufacturer_frame = ctk.CTkFrame(parent)
        manufacturer_frame.pack(anchor="w", pady=(0, 5))

        # Manufacturer label
        manufacturer_label = ctk.CTkLabel(
            manufacturer_frame,
            text="Manufacturer:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        manufacturer_label.pack(side="left", padx=(10, 5))

        # Manufacturer input field
        self.manufacturer_entry = ctk.CTkEntry(
            manufacturer_frame,
            placeholder_text="Enter Manufacturer...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.manufacturer_entry.pack(side="left", padx=(0, 10))

        # Reset button for Manufacturer
        self.reset_manufacturer_button = ctk.CTkButton(
            manufacturer_frame,
            text="Reset",
            command=self.reset_manufacturer,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            state="disabled"
        )
        self.reset_manufacturer_button.pack(side="left")

        # REMARK input field and buttons frame
        remark_frame = ctk.CTkFrame(parent)
        remark_frame.pack(anchor="w", pady=(0, 5))

        # REMARK label
        remark_label = ctk.CTkLabel(
            remark_frame,
            text="REMARK:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        remark_label.pack(side="left", padx=(10, 5))

        # REMARK input field
        self.remark_entry = ctk.CTkEntry(
            remark_frame,
            placeholder_text="Enter REMARK...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.remark_entry.pack(side="left", padx=(0, 10))

        # Reset button for REMARK
        self.reset_remark_button = ctk.CTkButton(
            remark_frame,
            text="Reset",
            command=self.reset_remark,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            state="disabled"
        )
        self.reset_remark_button.pack(side="left")

        # Separator after REMARK
        separator_parsed = ctk.CTkFrame(parent, height=self.SEPARATOR_HEIGHT)
        separator_parsed.pack(fill="x", padx=10, pady=10)

        # Type input field frame
        type_frame = ctk.CTkFrame(parent)
        type_frame.pack(anchor="w", pady=(0, 5))

        # Type label
        type_label = ctk.CTkLabel(
            type_frame,
            text="Type:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        type_label.pack(side="left", padx=(10, 5))

        # Type input field
        self.type_entry = ctk.CTkEntry(
            type_frame,
            placeholder_text="Parsed from User ERP Name...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.type_entry.pack(side="left", padx=(0, 10))
        # Bind to update User ERP Name when edited
        self.type_entry.bind('<KeyRelease>', self.on_parsed_field_change)

        # Convert underscores to hyphens button for Type
        self.convert_underscore_type_button = ctk.CTkButton(
            type_frame,
            text="_ → -",
            command=self.convert_underscores_to_hyphens_type,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.convert_underscore_type_button.pack(side="left")

        # PN (Part Number) input field frame
        pn_frame = ctk.CTkFrame(parent)
        pn_frame.pack(anchor="w", pady=(0, 5))

        # PN label
        pn_label = ctk.CTkLabel(
            pn_frame,
            text="PN:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        pn_label.pack(side="left", padx=(10, 5))

        # PN input field
        self.pn_entry = ctk.CTkEntry(
            pn_frame,
            placeholder_text="Parsed from User ERP Name...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.pn_entry.pack(side="left", padx=(0, 10))
        # Bind to update User ERP Name when edited
        self.pn_entry.bind('<KeyRelease>', self.on_parsed_field_change)

        # Convert underscores to hyphens button for PN
        self.convert_underscore_pn_button = ctk.CTkButton(
            pn_frame,
            text="_ → -",
            command=self.convert_underscores_to_hyphens_pn,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.convert_underscore_pn_button.pack(side="left", padx=(0, 5))
        
        # NO-PN button to insert "NO-PN" into PN field
        self.no_pn_button = ctk.CTkButton(
            pn_frame,
            text="NO-PN",
            command=self.insert_no_pn,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.no_pn_button.pack(side="left")

        # Details input field frame
        details_frame = ctk.CTkFrame(parent)
        details_frame.pack(anchor="w", pady=(0, 5))

        # Details label
        details_label = ctk.CTkLabel(
            details_frame,
            text="Details:",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.FIELD_LABEL_WIDTH
        )
        details_label.pack(side="left", padx=(10, 5))

        # Details input field
        self.details_entry = ctk.CTkEntry(
            details_frame,
            placeholder_text="Parsed from User ERP Name...",
            width=self.INPUT_FIELD_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.details_entry.pack(side="left", padx=(0, 10))
        # Bind to update User ERP Name when edited
        self.details_entry.bind('<KeyRelease>', self.on_parsed_field_change)

        # Convert underscores to hyphens button
        self.convert_underscore_button = ctk.CTkButton(
            details_frame,
            text="_ → -",
            command=self.convert_underscores_to_hyphens,
            width=self.RESET_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.convert_underscore_button.pack(side="left", padx=(0, 5))
        
        # Combined convert and update button
        self.convert_and_update_button = ctk.CTkButton(
            details_frame,
            text="_ → - + Update",
            command=self.convert_underscores_and_update_all,
            width=self.RESET_BUTTON_WIDTH + 20,
            height=self.BUTTON_HEIGHT
        )
        self.convert_and_update_button.pack(side="left")

        # Update button frame (moved to bottom)
        update_frame = ctk.CTkFrame(parent)
        update_frame.pack(anchor="w", pady=(5, 10))

        # Update button
        self.update_name_button = ctk.CTkButton(
            update_frame,
            text="Update All Fields",
            command=self.update_all_fields,
            width=self.UPDATE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT,
            state="disabled"
        )
        self.update_name_button.pack(side="left", padx=5)
        
        # Add Image button
        self.add_image_button = ctk.CTkButton(
            update_frame,
            text="Add Image",
            command=self.open_image_dialog,
            width=self.UPDATE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT,
            state="disabled"
        )
        self.add_image_button.pack(side="left", padx=5)
        
        # Delete button (moved here from top)
        self.delete_button = ctk.CTkButton(
            update_frame,
            text="Delete Selected Item",
            command=self.delete_selected_item,
            width=self.DELETE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT,
            fg_color="#d32f2f",  # Red color for delete action
            hover_color="#b71c1c",
            state="disabled"
        )
        self.delete_button.pack(side="left", padx=5)

    def setup_reassignment_section(self, parent):
        """Setup the reassignment section."""
        # Main container frame for two-column layout
        main_frame = ctk.CTkFrame(parent)
        main_frame.pack(fill="x", padx=10, pady=5)

        # Left column for dropdowns
        left_column = ctk.CTkFrame(main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

        # Category dropdown
        category_frame = ctk.CTkFrame(left_column)
        category_frame.pack(fill="x", pady=2)

        category_label = ctk.CTkLabel(category_frame, text="Category:", width=self.DROPDOWN_LABEL_WIDTH)
        category_label.pack(side="left", padx=(10, 5), pady=5)

        self.category_dropdown = ctk.CTkOptionMenu(
            category_frame,
            values=["Select Category..."],
            command=self.on_category_change,
            width=self.DROPDOWN_WIDTH
        )
        self.category_dropdown.pack(side="left", padx=5, pady=5)

        # Subcategory dropdown
        subcategory_frame = ctk.CTkFrame(left_column)
        subcategory_frame.pack(fill="x", pady=2)

        subcategory_label = ctk.CTkLabel(subcategory_frame, text="Subcategory:", width=self.DROPDOWN_LABEL_WIDTH)
        subcategory_label.pack(side="left", padx=(10, 5), pady=5)

        self.subcategory_dropdown = ctk.CTkOptionMenu(
            subcategory_frame,
            values=["Select Subcategory..."],
            command=self.on_subcategory_change,
            width=self.DROPDOWN_WIDTH
        )
        self.subcategory_dropdown.pack(side="left", padx=5, pady=5)

        # Sublevel dropdown
        sublevel_frame = ctk.CTkFrame(left_column)
        sublevel_frame.pack(fill="x", pady=2)

        sublevel_label = ctk.CTkLabel(sublevel_frame, text="Sublevel:", width=self.DROPDOWN_LABEL_WIDTH)
        sublevel_label.pack(side="left", padx=(10, 5), pady=5)

        self.sublevel_dropdown = ctk.CTkOptionMenu(
            sublevel_frame,
            values=["Select Sublevel..."],
            width=self.DROPDOWN_WIDTH
        )
        self.sublevel_dropdown.pack(side="left", padx=5, pady=5)

        # Right column for Reassign button
        right_column = ctk.CTkFrame(main_frame)
        right_column.pack(side="right", padx=(5, 10), pady=5)

        # Reassign button
        self.reassign_button = ctk.CTkButton(
            right_column,
            text="Reassign",
            command=self.reassign_item,
            width=self.REASSIGN_BUTTON_WIDTH,
            height=self.REASSIGN_BUTTON_HEIGHT,  # Spans multiple dropdown rows
            state="disabled"
        )
        self.reassign_button.pack(pady=5)

    def setup_data_cleaning_section(self, parent):
        """Setup the data cleaning section."""
        # Data cleaning frame at the bottom
        cleaning_frame = ctk.CTkFrame(parent)
        cleaning_frame.pack(fill="x", pady=(20, 0))

        # Title
        cleaning_title = ctk.CTkLabel(
            cleaning_frame,
            text="Data Cleaning Operations",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        cleaning_title.pack(pady=(10, 10))

        # Buttons frame
        buttons_frame = ctk.CTkFrame(cleaning_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Convert Multiline button
        self.convert_multiline_button = ctk.CTkButton(
            buttons_frame,
            text="Convert Multiline Cells",
            command=self.convert_multiline_cells,
            width=self.ACTION_BUTTON_WIDTH,
            state="disabled"
        )
        self.convert_multiline_button.pack(side="left", padx=5, pady=5)

        # Remove NEN button
        self.remove_nen_button = ctk.CTkButton(
            buttons_frame,
            text="Remove NEN Prefix",
            command=self.remove_nen_prefix,
            width=self.ACTION_BUTTON_WIDTH,
            state="disabled"
        )
        self.remove_nen_button.pack(side="left", padx=5, pady=5)

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
            # Populate User ERP Name field - priority: user modifications > original User ERP Name > ERP name
            erp_name = item_data.get('ERP name', '')

            # First check if user has made modifications
            current_user_name = self.tree_view.user_modifications.get(row_id, {}).get('user_erp_name', '')

            # If no user modifications, check if User ERP Name exists in original data
            if not current_user_name:
                current_user_name = item_data.get('User ERP Name', '')

            # If still no value, fall back to ERP name
            if not current_user_name:
                current_user_name = erp_name

            self.user_erp_name_entry.delete(0, tk.END)
            self.user_erp_name_entry.insert(0, current_user_name)

            # Parse User ERP Name into Type, PN, and Details
            self.parse_user_erp_name(current_user_name)

            # Populate Manufacturer field - priority: user modifications > original Manufacturer
            current_manufacturer = self.tree_view.user_modifications.get(row_id, {}).get('manufacturer', '')
            if not current_manufacturer:
                current_manufacturer = item_data.get('Manufacturer', '')

            self.manufacturer_entry.delete(0, tk.END)
            self.manufacturer_entry.insert(0, current_manufacturer)

            # Populate REMARK field - priority: user modifications > original REMARK
            current_remark = self.tree_view.user_modifications.get(row_id, {}).get('remark', '')
            if not current_remark:
                current_remark = item_data.get('REMARK', '')

            self.remark_entry.delete(0, tk.END)
            self.remark_entry.insert(0, current_remark)

            # Enable buttons when item is selected
            self.update_name_button.configure(state="normal")
            self.reset_name_button.configure(state="normal")
            self.reset_manufacturer_button.configure(state="normal")
            self.reset_remark_button.configure(state="normal")
            self.delete_button.configure(state="normal")
            self.add_image_button.configure(state="normal")

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
            self.reassign_button.configure(state="normal")
            
            # Update image preview
            self.update_image_preview()
        else:
            # Clear fields and disable buttons
            self.user_erp_name_entry.delete(0, tk.END)
            self.user_erp_name_entry.insert(0, "")
            self.manufacturer_entry.delete(0, tk.END)
            self.manufacturer_entry.insert(0, "")
            self.remark_entry.delete(0, tk.END)
            self.remark_entry.insert(0, "")
            
            # Clear parsed fields
            self.type_entry.delete(0, tk.END)
            self.pn_entry.delete(0, tk.END)
            self.details_entry.delete(0, tk.END)

            # Disable buttons when no item is selected
            self.update_name_button.configure(state="disabled")
            self.reset_name_button.configure(state="disabled")
            self.reset_manufacturer_button.configure(state="disabled")
            self.reset_remark_button.configure(state="disabled")
            self.delete_button.configure(state="disabled")
            self.reassign_button.configure(state="disabled")
            self.add_image_button.configure(state="disabled")

            # Reset dropdowns
            self.category_dropdown.configure(values=["Select Category..."])
            self.subcategory_dropdown.configure(values=["Select Subcategory..."])
            self.sublevel_dropdown.configure(values=["Select Sublevel..."])
            
            # Clear image preview
            self.update_image_preview()

    def parse_user_erp_name(self, user_erp_name):
        """Parse User ERP Name into Type, PN, and Details fields.
        
        Format: Type_PN_Details
        - Type: First string before first "_"
        - PN: String between first and second "_"
        - Details: Everything after second "_"
        """
        if not user_erp_name:
            # Clear all parsed fields
            self.type_entry.delete(0, tk.END)
            self.pn_entry.delete(0, tk.END)
            self.details_entry.delete(0, tk.END)
            return
        
        # Split by underscore
        parts = user_erp_name.split('_', 2)  # Split into maximum 3 parts
        
        # Extract Type (first part)
        type_value = parts[0] if len(parts) > 0 else ""
        self.type_entry.delete(0, tk.END)
        self.type_entry.insert(0, type_value)
        
        # Extract PN (second part)
        pn_value = parts[1] if len(parts) > 1 else ""
        self.pn_entry.delete(0, tk.END)
        self.pn_entry.insert(0, pn_value)
        
        # Extract Details (everything after second underscore)
        details_value = parts[2] if len(parts) > 2 else ""
        self.details_entry.delete(0, tk.END)
        self.details_entry.insert(0, details_value)

    def on_parsed_field_change(self, event=None):
        """Update User ERP Name when any of the parsed fields (Type, PN, Details) are edited."""
        # Get current values from parsed fields
        type_value = self.type_entry.get()
        pn_value = self.pn_entry.get()
        details_value = self.details_entry.get()
        
        # Reconstruct User ERP Name using underscore separator
        parts = []
        if type_value:
            parts.append(type_value)
        if pn_value:
            parts.append(pn_value)
        if details_value:
            parts.append(details_value)
        
        # Join with underscores
        new_user_erp_name = '_'.join(parts)
        
        # Update User ERP Name field
        self.user_erp_name_entry.delete(0, tk.END)
        self.user_erp_name_entry.insert(0, new_user_erp_name)

    def on_user_erp_name_change(self, event=None):
        """Re-parse User ERP Name into Type, PN, and Details when directly edited."""
        user_erp_name = self.user_erp_name_entry.get()
        self.parse_user_erp_name(user_erp_name)

    def open_image_dialog(self):
        """Open the image selection dialog."""
        if not self.selected_item or not self.selected_row_id:
            messagebox.showwarning("Warning", "Please select an item first")
            return
        
        # Initialize image handler if needed
        if not self.image_handler and self.main_window:
            from src.backend.image_handler import ImageHandler
            excel_path = self.main_window.current_file_path
            self.image_handler = ImageHandler(excel_path)
        
        # Get PN for initial search
        pn_value = self.pn_entry.get().strip()
        initial_search = pn_value if pn_value else self.selected_item.get('ERP name', '')
        
        # Open image dialog
        from src.gui.image_dialog import ImageSelectionDialog
        ImageSelectionDialog(
            self.main_window.root if self.main_window else self,
            self.image_handler,
            initial_search,
            callback=self.on_image_selected
        )
    
    def on_image_selected(self, relative_path: str):
        """Callback when image is selected and saved.
        
        Args:
            relative_path: Relative path to the saved image
        """
        if not self.selected_row_id:
            return
        
        # Update the Image column in user modifications
        if self.selected_row_id not in self.tree_view.user_modifications:
            self.tree_view.user_modifications[self.selected_row_id] = {}
        self.tree_view.user_modifications[self.selected_row_id]['image'] = relative_path
        
        # Update the image preview
        self.load_and_display_image(relative_path)
        
        # Update status
        if self.main_window and hasattr(self.main_window, 'update_status'):
            self.main_window.update_status(f"Image added: {relative_path}")
    
    def load_and_display_image(self, image_path: str):
        """Load and display an image in the preview area.
        
        Args:
            image_path: Relative or absolute path to the image
        """
        if not image_path:
            # Show "No Image" placeholder
            self.image_preview_label.configure(image='', text="No Image")
            self.current_image_photo = None
            return
        
        try:
            # Initialize image handler if needed
            if not self.image_handler and self.main_window:
                from src.backend.image_handler import ImageHandler
                excel_path = self.main_window.current_file_path
                self.image_handler = ImageHandler(excel_path)
            
            # Load image
            if self.image_handler:
                image = self.image_handler.load_image(image_path)
                
                if image:
                    # Resize for preview
                    image.thumbnail((self.IMAGE_PREVIEW_SIZE, self.IMAGE_PREVIEW_SIZE), Image.Resampling.LANCZOS)
                    
                    # Convert to PhotoImage
                    photo = ImageTk.PhotoImage(image)
                    
                    # Update label
                    self.image_preview_label.configure(image=photo, text="")
                    self.current_image_photo = photo  # Keep reference
                else:
                    self.image_preview_label.configure(image='', text="Image\nNot Found")
            else:
                self.image_preview_label.configure(image='', text="No Image")
                
        except Exception as e:
            print(f"Error displaying image: {e}")
            self.image_preview_label.configure(image='', text="Error\nLoading")
    
    def update_image_preview(self):
        """Update image preview based on selected item."""
        if self.selected_item and self.selected_row_id:
            # Check if there's a modified image path
            image_path = self.tree_view.user_modifications.get(
                self.selected_row_id, {}
            ).get('image', '')
            
            # If no modification, check original data
            if not image_path:
                image_path = self.selected_item.get('Image', '')
            
            # Load and display
            self.load_and_display_image(image_path)
        else:
            # Multiple items or no selection - show placeholder
            if hasattr(self.tree_view, 'selected_items') and len(self.tree_view.selected_items) > 1:
                self.image_preview_label.configure(image='', text="Multiple\nItems")
                self.current_image_photo = None
            else:
                self.image_preview_label.configure(image='', text="No Image")
                self.current_image_photo = None

    def convert_underscores_to_hyphens_type(self):
        """Convert all underscore characters to hyphens in the Type field."""
        # Get current Type value
        type_value = self.type_entry.get()
        
        # Replace all underscores with hyphens
        converted_value = type_value.replace('_', '-')
        
        # Update Type field
        self.type_entry.delete(0, tk.END)
        self.type_entry.insert(0, converted_value)
        
        # This will trigger on_parsed_field_change to update User ERP Name
        self.on_parsed_field_change()

    def convert_underscores_to_hyphens_pn(self):
        """Convert all underscore characters to hyphens in the PN field."""
        # Get current PN value
        pn_value = self.pn_entry.get()
        
        # Replace all underscores with hyphens
        converted_value = pn_value.replace('_', '-')
        
        # Update PN field
        self.pn_entry.delete(0, tk.END)
        self.pn_entry.insert(0, converted_value)
        
        # This will trigger on_parsed_field_change to update User ERP Name
        self.on_parsed_field_change()

    def insert_no_pn(self):
        """Insert 'NO-PN' into the PN field."""
        # Clear and insert "NO-PN"
        self.pn_entry.delete(0, tk.END)
        self.pn_entry.insert(0, "NO-PN")
        
        # This will trigger on_parsed_field_change to update User ERP Name
        self.on_parsed_field_change()

    def convert_underscores_to_hyphens(self):
        """Convert all underscore characters to hyphens in the Details field."""
        # Get current Details value
        details_value = self.details_entry.get()
        
        # Replace all underscores with hyphens
        converted_value = details_value.replace('_', '-')
        
        # Update Details field
        self.details_entry.delete(0, tk.END)
        self.details_entry.insert(0, converted_value)
        
        # This will trigger on_parsed_field_change to update User ERP Name
        self.on_parsed_field_change()

    def convert_underscores_and_update_all(self):
        """Convert underscores to hyphens in Details field and update all fields."""
        # First, convert underscores to hyphens in Details field
        self.convert_underscores_to_hyphens()
        
        # Then, update all fields
        self.update_all_fields()

    def delete_selected_item(self):
        """Delete the selected item from the tree view."""
        if not self.selected_row_id or not self.selected_item:
            return

        # Show confirmation dialog
        result = messagebox.askyesno(
            "Delete Item",
            f"Are you sure you want to delete this item?\n\n"
            f"ERP Name: {self.selected_item.get('ERP name', 'Unknown')}\n"
            f"Category: {self.selected_item.get('Article Category', 'Unknown')}\n"
            f"Subcategory: {self.selected_item.get('Article Subcategory', 'Unknown')}\n"
            f"Sublevel: {self.selected_item.get('Article Sublevel', 'Unknown')}\n\n"
            f"This action cannot be undone.",
            icon="warning"
        )

        if result:
            # Delete the item from tree view
            self.tree_view.delete_item(self.selected_row_id)

            # Clear the edit panel
            self.set_selected_item(None, None)

            # Update status
            if self.main_window and hasattr(self.main_window, 'update_status'):
                self.main_window.update_status("Item deleted successfully")

    def update_all_fields(self):
        """Update all fields (User ERP Name, Manufacturer, REMARK) for the selected item."""
        if not self.selected_row_id:
            return

        # Get values from all input fields
        user_erp_name = self.user_erp_name_entry.get().strip()
        manufacturer = self.manufacturer_entry.get().strip()
        remark = self.remark_entry.get().strip()

        # Update all fields in tree view
        self.tree_view.update_user_erp_name(self.selected_row_id, user_erp_name)
        self.tree_view.update_manufacturer(self.selected_row_id, manufacturer)
        self.tree_view.update_remark(self.selected_row_id, remark)

        # Update status if main window is available
        if self.main_window and hasattr(self.main_window, 'status_label'):
            updated_fields = []
            if user_erp_name:
                updated_fields.append(f"ERP name: {user_erp_name}")
            if manufacturer:
                updated_fields.append(f"Manufacturer: {manufacturer}")
            if remark:
                updated_fields.append(f"REMARK: {remark}")

            if updated_fields:
                self.main_window.update_status(f"Updated: {', '.join(updated_fields)}")
            else:
                self.main_window.update_status("Cleared all field values")

    def reset_user_erp_name(self):
        """Reset the user ERP name for the selected item to original ERP name."""
        if not self.selected_row_id or not self.selected_item:
            return

        # Get the original ERP name
        original_erp_name = self.selected_item.get('ERP name', '')

        # Clear the user ERP name (set to empty string to reset to original)
        self.tree_view.update_user_erp_name(self.selected_row_id, '')

        # Update the input field to show the original ERP name
        self.user_erp_name_entry.delete(0, tk.END)
        self.user_erp_name_entry.insert(0, original_erp_name)

        # Update status if main window is available
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Reset ERP name to original: {original_erp_name}")

    def reset_manufacturer(self):
        """Reset the manufacturer for the selected item to original value."""
        if not self.selected_row_id or not self.selected_item:
            return

        # Get original manufacturer
        original_manufacturer = self.selected_item.get('Manufacturer', '')

        # Clear the entry and insert original manufacturer
        self.manufacturer_entry.delete(0, tk.END)
        self.manufacturer_entry.insert(0, original_manufacturer)

        # Update the tree view
        self.tree_view.update_manufacturer(self.selected_row_id, original_manufacturer)

        # Update status if main window is available
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Reset Manufacturer to: {original_manufacturer}")

    def reset_remark(self):
        """Reset the remark for the selected item to original value."""
        if not self.selected_row_id or not self.selected_item:
            return

        # Get original remark
        original_remark = self.selected_item.get('REMARK', '')

        # Clear the entry and insert original remark
        self.remark_entry.delete(0, tk.END)
        self.remark_entry.insert(0, original_remark)

        # Update the tree view
        self.tree_view.update_remark(self.selected_row_id, original_remark)

        # Update status if main window is available
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Reset REMARK to: {original_remark}")

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
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Reassigned item to: {category} > {subcategory} > {sublevel}")

    def convert_multiline_cells(self):
        """Convert multiline cells to single line entries."""
        if not hasattr(self.main_window, 'excel_handler') or self.main_window.excel_handler is None:
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
            if self.main_window and hasattr(self.main_window, 'update_status'):
                self.main_window.update_status("Multiline conversion cancelled")
            return

        # Show progress
        if self.main_window and hasattr(self.main_window, 'update_status'):
            self.main_window.update_status("Converting multiline cells to single line...")

        # Perform the conversion
        try:
            result = self.main_window.excel_handler.convert_multiline_to_single_line()

            # Reload the tree view with the updated data from Excel handler
            self.tree_view.load_data(self.main_window.excel_handler.get_data())

            # Update status with results
            if result["converted"] > 0:
                if self.main_window and hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status(
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
                if self.main_window and hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status("No multiline cells found to convert")
                messagebox.showinfo("No Conversion Needed", "No multiline cells were found in the data.")

        except Exception as e:
            error_msg = f"Error converting multiline cells: {str(e)}"
            if self.main_window and hasattr(self.main_window, 'update_status'):
                self.main_window.update_status(error_msg)
            messagebox.showerror("Conversion Error", error_msg)

    def remove_nen_prefix(self):
        """Remove 'NEN' prefix and subsequent spaces from all cells."""
        if not hasattr(self.main_window, 'excel_handler') or self.main_window.excel_handler is None:
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
            if self.main_window and hasattr(self.main_window, 'update_status'):
                self.main_window.update_status("NEN removal cancelled")
            return

        # Show progress
        if self.main_window and hasattr(self.main_window, 'update_status'):
            self.main_window.update_status("Removing 'NEN' prefix from cells...")

        # Perform the removal
        try:
            result = self.main_window.excel_handler.remove_nen_prefix()

            # Reload the tree view with the updated data from Excel handler
            self.tree_view.load_data(self.main_window.excel_handler.get_data())

            # Update status with results
            if result["converted"] > 0:
                if self.main_window and hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status(
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
                if self.main_window and hasattr(self.main_window, 'update_status'):
                    self.main_window.update_status("No cells with 'NEN' prefix found")
                messagebox.showinfo("No NEN Prefix Found", "No cells starting with 'NEN' were found in the data.")

        except Exception as e:
            error_msg = f"Error removing 'NEN' prefix: {str(e)}"
            if self.main_window and hasattr(self.main_window, 'update_status'):
                self.main_window.update_status(error_msg)
            messagebox.showerror("NEN Removal Error", error_msg)
