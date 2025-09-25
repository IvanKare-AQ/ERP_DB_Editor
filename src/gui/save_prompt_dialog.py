"""
Save Prompt Dialog for saving AI prompts.
"""
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from typing import Optional, Callable
from src.backend.prompt_manager import PromptManager


class SavePromptDialog:
    """Dialog for saving AI prompts."""
    
    def __init__(self, parent, prompt_text: str, on_prompt_saved: Optional[Callable] = None, 
                 initial_name: str = "", initial_description: str = "", 
                 is_rename: bool = False, old_name: str = ""):
        """Initialize the save prompt dialog.
        
        Args:
            parent: Parent window
            prompt_text: The prompt text to save
            on_prompt_saved: Callback function called when prompt is saved
            initial_name: Initial name for the prompt
            initial_description: Initial description for the prompt
            is_rename: Whether this is a rename operation
            old_name: Original name (for rename operations)
        """
        self.parent = parent
        self.prompt_text = prompt_text
        self.on_prompt_saved = on_prompt_saved
        self.prompt_manager = PromptManager()
        self.is_rename = is_rename
        self.old_name = old_name
        self.initial_name = initial_name
        self.initial_description = initial_description
        
        # Create the dialog window
        self.dialog = ctk.CTkToplevel(parent)
        if self.is_rename:
            self.dialog.title("Rename AI Prompt")
        else:
            self.dialog.title("Save AI Prompt")
        self.dialog.geometry("700x600")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Create the UI
        self.create_widgets()
    
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
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        if self.is_rename:
            title_text = "Rename AI Prompt"
        else:
            title_text = "Save AI Prompt"
            
        title_label = ctk.CTkLabel(
            main_frame,
            text=title_text,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Prompt name input
        name_frame = ctk.CTkFrame(main_frame)
        name_frame.pack(fill="x", pady=(0, 10))
        
        name_label = ctk.CTkLabel(name_frame, text="Prompt Name:", 
                                font=ctk.CTkFont(size=12, weight="bold"))
        name_label.pack(pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="Enter a name for this prompt...",
            height=35
        )
        self.name_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Description input
        desc_frame = ctk.CTkFrame(main_frame)
        desc_frame.pack(fill="x", pady=(0, 10))
        
        desc_label = ctk.CTkLabel(desc_frame, text="Description:", 
                                font=ctk.CTkFont(size=12, weight="bold"))
        desc_label.pack(pady=(10, 5))
        
        self.desc_entry = ctk.CTkEntry(
            desc_frame,
            placeholder_text="Brief description of what this prompt does...",
            height=35
        )
        self.desc_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Prompt preview
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        preview_label = ctk.CTkLabel(preview_frame, text="Prompt Preview:", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(10, 5))
        
        self.preview_text = ctk.CTkTextbox(
            preview_frame,
            height=150,
            font=ctk.CTkFont(family="Courier", size=10)
        )
        self.preview_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.preview_text.insert("1.0", self.prompt_text)
        self.preview_text.configure(state="disabled")  # Make read-only
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, height=80)
        buttons_frame.pack(fill="x", pady=(20, 20))
        buttons_frame.pack_propagate(False)
        
        # Save button
        if self.is_rename:
            save_button_text = "Rename Prompt"
        else:
            save_button_text = "Save Prompt"
            
        self.save_button = ctk.CTkButton(
            buttons_frame,
            text=save_button_text,
            command=self.save_prompt,
            width=150,
            height=40,
            state="disabled",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.save_button.pack(side="left", padx=(20, 10), pady=10)
        
        # Cancel button
        self.cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.close_dialog,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.cancel_button.pack(side="right", padx=(10, 20), pady=10)
        
        # Bind events
        self.name_entry.bind('<KeyRelease>', self.on_input_change)
        self.desc_entry.bind('<KeyRelease>', self.on_input_change)
        
        # Set initial values
        self.name_entry.insert(0, self.initial_name)
        self.desc_entry.insert(0, self.initial_description)
        
        # Update button state based on initial values
        self.on_input_change()
        
        # Focus on name entry
        self.name_entry.focus()
    
    def on_input_change(self, event=None):
        """Handle input field changes to enable/disable save button."""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        # Enable save button only if both fields have content
        if name and description:
            self.save_button.configure(state="normal")
        else:
            self.save_button.configure(state="disabled")
    
    def save_prompt(self):
        """Save the prompt."""
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if not name or not description:
            messagebox.showwarning("Warning", "Please fill in both name and description.")
            return
        
        # Handle rename operation
        if self.is_rename and self.old_name:
            # For rename, delete the old prompt if the name changed
            if name != self.old_name:
                if self.prompt_manager.prompt_exists(name):
                    response = messagebox.askyesno(
                        "Prompt Exists",
                        f"A prompt with the name '{name}' already exists.\n\nDo you want to overwrite it?"
                    )
                    if not response:
                        return
                
                # Delete the old prompt
                self.prompt_manager.delete_prompt(self.old_name)
        else:
            # For regular save, check if prompt exists
            if self.prompt_manager.prompt_exists(name):
                response = messagebox.askyesno(
                    "Prompt Exists",
                    f"A prompt with the name '{name}' already exists.\n\nDo you want to overwrite it?"
                )
                if not response:
                    return
        
        # Save the prompt
        if self.prompt_manager.save_prompt(name, description, self.prompt_text):
            if self.is_rename:
                messagebox.showinfo("Success", f"Prompt renamed to '{name}' successfully!")
            else:
                messagebox.showinfo("Success", f"Prompt '{name}' saved successfully!")
            
            # Call callback if provided
            if self.on_prompt_saved:
                self.on_prompt_saved()
            
            self.close_dialog()
        else:
            if self.is_rename:
                messagebox.showerror("Error", "Failed to rename prompt. Please try again.")
            else:
                messagebox.showerror("Error", "Failed to save prompt. Please try again.")
    
    def close_dialog(self):
        """Close the dialog."""
        self.dialog.destroy()
