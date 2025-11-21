"""
Add Item Editor Tab for ERP Database Editor
Extends the manual editor to support creating new draft items.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Any, Dict

from src.gui.manual_editor import ManualEditor


class AddEditor(ManualEditor):
    """Add tab implementation built on top of the manual editor."""

    def __init__(self, parent, tree_view, main_window=None):
        super().__init__(parent, tree_view, main_window, mode="add")
        self.selected_image_path = ""

        self._customize_for_add_mode()
        self.load_categories()
        self.reset_form_fields()

    # ------------------------------------------------------------------
    # UI Customization
    # ------------------------------------------------------------------
    def _customize_for_add_mode(self) -> None:
        """Adjust the inherited manual editor UI for add-mode specifics."""
        if hasattr(self, "title_label"):
            self.title_label.configure(text="Add Items")

        self._setup_image_action_row()

        if hasattr(self, "reassign_button"):
            self.reassign_button.configure(text="Reassign", command=self.reassign_item)

        if hasattr(self, "reassign_button_container") and hasattr(self, "reassign_button"):
            self.reassign_button.pack_forget()
            self.suggest_button = ctk.CTkButton(
                self.reassign_button_container,
                text="Suggest",
                command=self.suggest_category,
                width=self.REASSIGN_BUTTON_WIDTH,
                height=32,
                state="normal"
            )
            self.suggest_button.pack(pady=(0, 5))
            self.reassign_button.pack(pady=5)

    def _setup_image_action_row(self) -> None:
        """Create the horizontal row of Import / Add Item / Add Image buttons beneath the image preview."""
        if hasattr(self, "add_image_button"):
            self.add_image_button.destroy()

        self.image_action_frame = ctk.CTkFrame(self)
        pack_kwargs = {"pady": (0, 15)}
        if hasattr(self, "user_erp_frame") and self.user_erp_frame is not None:
            pack_kwargs["before"] = self.user_erp_frame
        self.image_action_frame.pack(**pack_kwargs)

        self.add_item_button = ctk.CTkButton(
            self.image_action_frame,
            text="<- Add Item",
            command=self.add_new_item,
            width=self.UPDATE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.add_item_button.pack(side="left", padx=5)

        self.import_button = ctk.CTkButton(
            self.image_action_frame,
            text="Import",
            command=self.import_item,
            width=self.UPDATE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.import_button.pack(side="left", padx=5)

        self.add_image_button = ctk.CTkButton(
            self.image_action_frame,
            text="Add Image",
            command=self.open_image_dialog,
            width=self.UPDATE_BUTTON_WIDTH,
            height=self.INPUT_FIELD_HEIGHT
        )
        self.add_image_button.pack(side="left", padx=5)

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------
    def set_selected_item(self, item_data, row_id):
        """Allow editing of selected draft items just like the manual tab."""
        super().set_selected_item(item_data, row_id)

        if item_data:
            self.selected_image_path = item_data.get('Image', '') or ''
        else:
            self.selected_image_path = ""

    def reset_user_erp_name(self):
        """Clear ERP name instead of restoring from a selected row."""
        self.user_erp_name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.pn_entry.delete(0, tk.END)
        self.details_entry.delete(0, tk.END)
        self.selected_image_path = ""
        self.image_preview_label.configure(image='', text="No Image")

    def reset_manufacturer(self):
        """Clear manufacturer input."""
        self.manufacturer_entry.delete(0, tk.END)

    def reset_remark(self):
        """Clear remark input."""
        self.remark_entry.delete(0, tk.END)

    def open_image_dialog(self):
        """Open the image selection dialog without depending on a selected row."""
        if not self.main_window:
            messagebox.showwarning("Warning", "Main window not available.")
            return

        if not self.image_handler:
            from src.backend.image_handler import ImageHandler
            db_path = self.main_window.current_file_path
            self.image_handler = ImageHandler(db_path)

        # Prefer PN for the search seed; fall back to ERP name
        pn_value = self.pn_entry.get().strip()
        initial_search = pn_value if pn_value else self.user_erp_name_entry.get().strip()

        from src.gui.image_dialog import ImageSelectionDialog

        ImageSelectionDialog(
            self.main_window.root if hasattr(self.main_window, "root") else self,
            self.image_handler,
            initial_search,
            callback=self.on_image_selected
        )

    def on_image_selected(self, relative_path: str):
        """Store the chosen image path for the new draft item."""
        self.selected_image_path = relative_path
        self.load_and_display_image(relative_path)
        if self.main_window and hasattr(self.main_window, 'update_status'):
            self.main_window.update_status(f"Image selected: {relative_path}")

    def delete_selected_item(self):
        """Draft deletion is not implemented yet."""
        messagebox.showinfo("Not Available", "Draft deletion will be available in a future update.")

    # ------------------------------------------------------------------
    # Draft Item Workflow
    # ------------------------------------------------------------------
    def reset_form_fields(self):
        """Return all fields to their default empty state."""
        self.selected_image_path = ""
        self.user_erp_name_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.pn_entry.delete(0, tk.END)
        self.details_entry.delete(0, tk.END)
        self.manufacturer_entry.delete(0, tk.END)
        self.remark_entry.delete(0, tk.END)

        self.image_preview_label.configure(image='', text="No Image")
        self.current_image_photo = None

        # Reset dropdowns to placeholders
        self.category_dropdown.set("Select Category...")
        self.subcategory_dropdown.set("Select Subcategory...")
        self.subcategory_dropdown.configure(values=["Select Subcategory..."])
        self.sub_subcategory_dropdown.set("Select Sub-subcategory...")
        self.sub_subcategory_dropdown.configure(values=["Select Sub-subcategory..."])

        if hasattr(self, "add_item_button"):
            self.add_item_button.configure(state="normal")

    def import_item(self):
        """Placeholder for future import capability."""
        messagebox.showinfo("Coming Soon", "Importing items will be available in a future update.")

    def suggest_category(self):
        """Placeholder for AI suggestion flow."""
        messagebox.showinfo("Suggestion", "Suggestions will be provided in a future update.")

    def add_new_item(self):
        """Validate inputs, build a draft item, and persist it to the temporary JSON."""
        if not self.main_window or not hasattr(self.main_window, "json_handler"):
            messagebox.showerror("Error", "JSON handler not available.")
            return

        full_name = self.user_erp_name_entry.get().strip()
        category = self.category_dropdown.get().strip()
        subcategory = self.subcategory_dropdown.get().strip()
        sub_subcategory = self.sub_subcategory_dropdown.get().strip()

        if not full_name:
            messagebox.showwarning("Missing Data", "ERP Name is required.")
            return

        placeholder_values = {"Select Category...", "Select Subcategory...", "Select Sub-subcategory..."}
        if (
            not category
            or not subcategory
            or not sub_subcategory
            or category in placeholder_values
            or subcategory in placeholder_values
            or sub_subcategory in placeholder_values
        ):
            messagebox.showwarning("Missing Data", "Please choose Category, Subcategory, and Sub-subcategory.")
            return

        json_handler = self.main_window.json_handler
        pn_value = json_handler.get_next_available_pn()
        item_payload = self._build_new_item_payload(pn_value, category, subcategory, sub_subcategory)

        json_handler.add_added_item(item_payload)
        json_handler.save_added_items()

        if hasattr(self.main_window, "refresh_added_items_view"):
            self.main_window.refresh_added_items_view()

        messagebox.showinfo("Draft Saved", f"Draft item PN {pn_value} saved to the add queue.")
        self.reset_form_fields()

    def _build_new_item_payload(
        self,
        pn_value: int,
        category: str,
        subcategory: str,
        sub_subcategory: str
    ) -> Dict[str, Any]:
        """Construct the JSON object for the new draft item."""
        erp_name_obj = {
            'full_name': self.user_erp_name_entry.get().strip(),
            'type': self.type_entry.get().strip(),
            'part_number': self.pn_entry.get().strip(),
            'additional_parameters': self.details_entry.get().strip()
        }

        manufacturer = self.manufacturer_entry.get().strip()
        remark = self.remark_entry.get().strip()

        props = {}
        if hasattr(self.main_window, "json_handler"):
            props = self.main_window.json_handler.get_category_properties(category, subcategory, sub_subcategory) or {}

        new_item = {
            'PN': pn_value,
            'ERP Name': erp_name_obj,
            'Image': self.selected_image_path,
            'Manufacturer': manufacturer,
            'Remark': remark,
            'Tracking Method': '',
            'Use for ML': False,
            'Category': category,
            'Subcategory': subcategory,
            'Sub-subcategory': sub_subcategory,
            'Stage': props.get('stage', ''),
            'Origin': props.get('origin', ''),
            'Serialized': props.get('serialized', ''),
            'Usage': props.get('usage', ''),
            'CAD Name': '',
            'EAN13': ''
        }

        return new_item

