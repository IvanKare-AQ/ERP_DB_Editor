"""
Tabbed Edit Panel for ERP Database Editor
Contains three tabs: Manual, AI, and ML editors.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from PIL import Image, ImageDraw

from src.gui.add_editor import AddEditor
from src.gui.manual_editor import ManualEditor
from src.gui.ai_editor import AIEditor
from src.gui.ml_editor import MLEditor


class EditPanel(ctk.CTkFrame):
    """Tabbed panel containing Manual, AI, and ML editors."""

    # Configuration constants
    PANEL_WIDTH = 750  # Fixed width to accommodate widest tab
    
    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the tabbed edit panel."""
        super().__init__(parent)
        
        self.tree_view = tree_view
        self.main_window = main_window

        # Panel will be sized by parent container

        # Create the tabbed interface
        self.create_tabbed_interface()
        
    def create_tabbed_interface(self):
        """Create the tabbed interface for Manual, AI, and ML editors."""
        # Create tabview with fixed width
        self.tabview = ctk.CTkTabview(self, width=self.PANEL_WIDTH)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Add tabs (ordering: Add, Manual, AI, ML)
        self.add_tab = self.tabview.add("Add")  # Add tab for database insertions with custom icon
        self.manual_tab = self.tabview.add("Manual ✏️")  # Manual tab with pencil icon
        self.ai_tab = self.tabview.add("AI 🤖")  # AI tab with robot icon
        self.ml_tab = self.tabview.add("ML 🧠")  # ML tab with brain icon

        # Create editors for each tab (without setting width since tabview controls it)
        self.add_editor = AddEditor(self.add_tab, self.tree_view, self.main_window)
        self.add_editor.pack(fill="both", expand=True)

        self.manual_editor = ManualEditor(self.manual_tab, self.tree_view, self.main_window)
        self.manual_editor.pack(fill="both", expand=True)

        self.ai_editor = AIEditor(self.ai_tab, self.tree_view, self.main_window)
        self.ai_editor.pack(fill="both", expand=True)

        self.ml_editor = MLEditor(self.ml_tab, self.tree_view, self.main_window)
        self.ml_editor.pack(fill="both", expand=True)
        self._apply_add_tab_icon()
            
    def set_selected_item(self, item_data, row_id):
        """Set the selected item for all editors."""
        self.add_editor.set_selected_item(item_data, row_id)
        self.manual_editor.set_selected_item(item_data, row_id)
        self.ai_editor.set_selected_item(item_data, row_id)
        self.ml_editor.set_selected_item(item_data, row_id)

    @classmethod
    def get_panel_width(cls):
        """Get the panel width - useful for external layout calculations."""
        return cls.PANEL_WIDTH

    def _create_add_tab_icon(self, size=16, line_width=2):
        """Create a green plus icon for the Add tab."""
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        color = (76, 175, 80, 255)  # Material Green 500
        margin = size * 0.25
        center = size / 2
        draw.line((center, margin, center, size - margin), fill=color, width=line_width, joint="round")
        draw.line((margin, center, size - margin, center), fill=color, width=line_width, joint="round")
        return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))

    def _apply_add_tab_icon(self):
        """Attach the green plus icon to the Add tab button."""
        try:
            self._add_tab_icon = self._create_add_tab_icon()
            add_button = self.tabview._segmented_button._buttons_dict["Add"]
            add_button.configure(image=self._add_tab_icon, compound="right")
        except KeyError:
            # Fallback: tab label might be different if theme reorders or renames tabs
            pass
        
