"""
Add Item Editor Tab for ERP Database Editor
Provides a placeholder interface for adding new items to the database.
"""

import customtkinter as ctk


class AddEditor(ctk.CTkFrame):
    """Initial skeleton for the Add Item tab."""

    def __init__(self, parent, tree_view, main_window=None):
        super().__init__(parent)
        self.tree_view = tree_view
        self.main_window = main_window

        self.configure(padx=20, pady=20)

        self.title_label = ctk.CTkLabel(
            self,
            text="Add New Item",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(0, 10))

        self.description_label = ctk.CTkLabel(
            self,
            text=(
                "This tab will be used to add new items to the database.\n"
                "Future updates will include form fields for entering\n"
                "Category, Subcategory, Sub-subcategory, and ERP details."
            ),
            justify="left"
        )
        self.description_label.pack(anchor="w")

    def set_selected_item(self, item_data, row_id):
        """No-op for now; kept for interface consistency."""
        # This tab does not depend on the currently selected item yet.
        pass

