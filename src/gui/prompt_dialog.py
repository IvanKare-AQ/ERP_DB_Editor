"""
Prompt Selection Dialog for AI prompts management.
"""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional, Callable
from src.backend.prompt_manager import PromptManager


class PromptSelectionDialog:
    """Dialog for selecting and managing AI prompts."""
    
    def __init__(self, parent, on_prompt_selected: Callable[[str], None]):
        """Initialize the prompt selection dialog.
        
        Args:
            parent: Parent window
            on_prompt_selected: Callback function called when a prompt is selected
        """
        self.parent = parent
        self.on_prompt_selected = on_prompt_selected
        self.prompt_manager = PromptManager()
        self.selected_prompt = None
        
        # Create the dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Select AI Prompt")
        self.dialog.geometry("800x700")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create the UI
        self.create_widgets()
        
        # Load prompts
        self.load_prompts()
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create the dialog widgets."""
        # Main container
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Select AI Prompt",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Two-column layout
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left column - Prompt list
        left_frame = ctk.CTkFrame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        list_label = ctk.CTkLabel(left_frame, text="Saved Prompts:", 
                                font=ctk.CTkFont(size=12, weight="bold"))
        list_label.pack(pady=(5, 5))
        
        # Scrollable frame for prompt list
        self.prompt_list_frame = ctk.CTkScrollableFrame(left_frame, height=400)
        self.prompt_list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Right column - Prompt preview
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        preview_label = ctk.CTkLabel(right_frame, text="Prompt Preview:", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(5, 5))
        
        # Text widget for prompt preview (read-only)
        self.preview_text = ctk.CTkTextbox(
            right_frame,
            height=400,
            font=ctk.CTkFont(family="Courier", size=11)
        )
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=5)
        self.preview_text.configure(state="disabled")  # Make read-only
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Load to Editor button
        self.load_button = ctk.CTkButton(
            buttons_frame,
            text="Load to Editor",
            command=self.load_to_editor,
            width=100,
            height=30,
            state="disabled"
        )
        self.load_button.pack(side="left", padx=(10, 3))
        
        # Duplicate button
        self.duplicate_button = ctk.CTkButton(
            buttons_frame,
            text="Duplicate",
            command=self.duplicate_prompt,
            width=80,
            height=30,
            state="disabled"
        )
        self.duplicate_button.pack(side="left", padx=3)
        
        # Edit button
        self.edit_button = ctk.CTkButton(
            buttons_frame,
            text="Edit Prompt",
            command=self.edit_prompt,
            width=100,
            height=30,
            state="disabled"
        )
        self.edit_button.pack(side="left", padx=3)
        
        # Delete button
        self.delete_button = ctk.CTkButton(
            buttons_frame,
            text="Delete Prompt",
            command=self.delete_prompt,
            width=100,
            height=30,
            state="disabled"
        )
        self.delete_button.pack(side="left", padx=3)
        
        # Close button
        self.close_button = ctk.CTkButton(
            buttons_frame,
            text="Close",
            command=self.close_dialog,
            width=100,
            height=35
        )
        self.close_button.pack(side="right", padx=(5, 10))
    
    def load_prompts(self):
        """Load and display all saved prompts."""
        # Clear existing prompts
        for widget in self.prompt_list_frame.winfo_children():
            widget.destroy()
        
        prompts = self.prompt_manager.get_prompts()
        
        if not prompts:
            no_prompts_label = ctk.CTkLabel(
                self.prompt_list_frame,
                text="No saved prompts found.\nCreate some prompts first!",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            no_prompts_label.pack(pady=20)
            return
        
        # Create prompt buttons
        for name, prompt_data in prompts.items():
            self.create_prompt_button(name, prompt_data["description"])
    
    def create_prompt_button(self, name: str, description: str):
        """Create a button for a prompt.
        
        Args:
            name: Prompt name
            description: Prompt description
        """
        prompt_frame = ctk.CTkFrame(self.prompt_list_frame)
        prompt_frame.pack(fill="x", pady=2)
        
        # Store reference for highlighting
        prompt_frame.prompt_name = name
        
        # Prompt button
        prompt_button = ctk.CTkButton(
            prompt_frame,
            text=name,
            command=lambda n=name: self.on_prompt_clicked(n),
            height=35,
            anchor="w"
        )
        prompt_button.pack(fill="x", padx=5, pady=2)
        
        # Description label
        desc_label = ctk.CTkLabel(
            prompt_frame,
            text=description,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        desc_label.pack(fill="x", padx=5, pady=(0, 2))
    
    def clear_selection_highlighting(self):
        """Clear highlighting from all prompt frames."""
        for child in self.prompt_list_frame.winfo_children():
            if hasattr(child, 'prompt_name'):
                child.configure(fg_color=("gray90", "gray20"))  # Subtle default colors
    
    def highlight_selected_prompt(self, name: str):
        """Highlight the selected prompt frame."""
        for child in self.prompt_list_frame.winfo_children():
            if hasattr(child, 'prompt_name') and child.prompt_name == name:
                child.configure(fg_color=("lightgray", "gray30"))  # Subtle highlight colors
                break
    
    def on_prompt_clicked(self, name: str):
        """Handle prompt button click.
        
        Args:
            name: Name of the clicked prompt
        """
        # Clear previous selection highlighting
        self.clear_selection_highlighting()
        
        self.selected_prompt = name
        self.load_button.configure(state="normal")
        self.duplicate_button.configure(state="normal")
        self.edit_button.configure(state="normal")
        self.delete_button.configure(state="normal")
        
        # Highlight selected prompt
        self.highlight_selected_prompt(name)
        
        # Load and display the prompt
        prompt_text = self.prompt_manager.get_prompt(name)
        if prompt_text:
            self.preview_text.configure(state="normal")  # Enable editing temporarily
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", prompt_text)
            self.preview_text.configure(state="disabled")  # Make read-only again
    
    def load_to_editor(self):
        """Load the current prompt to the main editor and close dialog."""
        if self.selected_prompt and self.on_prompt_selected:
            prompt_text = self.prompt_manager.get_prompt(self.selected_prompt)
            if prompt_text:
                self.on_prompt_selected(prompt_text)
                self.close_dialog()
    
    def delete_prompt(self):
        """Delete the selected prompt."""
        if not self.selected_prompt:
            return
        
        # Confirm deletion
        response = messagebox.askyesno(
            "Delete Prompt",
            f"Are you sure you want to delete the prompt '{self.selected_prompt}'?\n\nThis action cannot be undone."
        )
        
        if response:
            if self.prompt_manager.delete_prompt(self.selected_prompt):
                messagebox.showinfo("Success", "Prompt deleted successfully.")
                self.selected_prompt = None
                self.load_button.configure(state="disabled")
                self.duplicate_button.configure(state="disabled")
                self.edit_button.configure(state="disabled")
                self.delete_button.configure(state="disabled")
                self.preview_text.delete("1.0", tk.END)
                self.load_prompts()  # Reload the list
            else:
                messagebox.showerror("Error", "Failed to delete prompt.")
    
    
    def edit_prompt(self):
        """Edit the selected prompt."""
        if not self.selected_prompt:
            return
        
        # Get current prompt data
        prompts = self.prompt_manager.get_prompts()
        current_prompt_data = prompts.get(self.selected_prompt, {})
        current_description = current_prompt_data.get("description", "")
        current_prompt_text = current_prompt_data.get("prompt", "")
        
        # Open edit prompt dialog with current data
        from src.gui.save_prompt_dialog import SavePromptDialog
        save_dialog = SavePromptDialog(
            self.dialog,
            current_prompt_text,
            initial_name=self.selected_prompt,
            initial_description=current_description,
            on_prompt_saved=self.on_prompt_saved,
            is_rename=True,
            old_name=self.selected_prompt
        )
    
    def duplicate_prompt(self):
        """Duplicate the selected prompt with a new name."""
        if not self.selected_prompt:
            return
        
        # Get current prompt data
        prompts = self.prompt_manager.get_prompts()
        current_prompt_data = prompts.get(self.selected_prompt, {})
        current_description = current_prompt_data.get("description", "")
        current_prompt_text = current_prompt_data.get("prompt", "")
        
        # Create new name with " - Copy" suffix
        new_name = f"{self.selected_prompt} - Copy"
        
        # Check if a prompt with this name already exists and add number if needed
        counter = 1
        original_new_name = new_name
        while self.prompt_manager.prompt_exists(new_name):
            new_name = f"{original_new_name} ({counter})"
            counter += 1
        
        # Save the duplicated prompt
        if self.prompt_manager.save_prompt(new_name, current_description, current_prompt_text):
            messagebox.showinfo("Success", f"Prompt duplicated successfully as '{new_name}'!")
            self.load_prompts()  # Reload to show changes
        else:
            messagebox.showerror("Error", "Failed to duplicate prompt.")
    
    def on_prompt_saved(self):
        """Callback when a prompt is saved."""
        # Clear highlighting
        self.clear_selection_highlighting()
        
        # Reload prompts to show changes
        self.load_prompts()
        
        # Clear selection
        self.selected_prompt = None
        self.load_button.configure(state="disabled")
        self.duplicate_button.configure(state="disabled")
        self.edit_button.configure(state="disabled")
        self.delete_button.configure(state="disabled")
        self.preview_text.delete("1.0", tk.END)
    
    def close_dialog(self):
        """Close the dialog."""
        self.dialog.destroy()
