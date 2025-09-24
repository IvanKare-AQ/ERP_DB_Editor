"""
Edit Panel for ERP Database Editor
Provides editing functionality for selected ERP items.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from src.backend.ollama_handler import OllamaHandler


class EditPanel(ctk.CTkFrame):
    """Panel for editing selected ERP items."""
    
    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the edit panel."""
        super().__init__(parent)
        
        self.tree_view = tree_view
        self.main_window = main_window
        self.selected_item = None
        self.selected_row_id = None
        
        # Initialize Ollama handler
        self.ollama_handler = OllamaHandler()
        self.available_models = []
        
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
        
        # Separator
        separator2 = ctk.CTkFrame(self, height=2)
        separator2.pack(fill="x", padx=10, pady=20)
        
        # AI Editing section
        self.setup_ai_editing_section()
        
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
        if self.main_window and hasattr(self.main_window, 'status_label'):
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
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Reassigned item to: {category} > {subcategory} > {sublevel}")
    
    def setup_ai_editing_section(self):
        """Setup the AI editing section."""
        # Section title
        section_title = ctk.CTkLabel(self, text="AI Editing", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        section_title.pack(pady=(0, 10))
        
        # AI Settings subsection
        ai_settings_frame = ctk.CTkFrame(self)
        ai_settings_frame.pack(fill="x", padx=10, pady=5)
        
        ai_settings_label = ctk.CTkLabel(ai_settings_frame, text="AI Settings:", 
                                       font=ctk.CTkFont(size=12, weight="bold"))
        ai_settings_label.pack(pady=(10, 5))
        
        # Model selection frame
        model_frame = ctk.CTkFrame(ai_settings_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        
        model_label = ctk.CTkLabel(model_frame, text="Model:", width=60)
        model_label.pack(side="left", padx=(10, 5), pady=10)
        
        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["No models available"],
            width=150
        )
        self.model_dropdown.pack(side="left", padx=5, pady=10)
        
        # Model control buttons
        self.refresh_models_button = ctk.CTkButton(
            model_frame,
            text="Refresh",
            command=self.refresh_models,
            width=60,
            height=25
        )
        self.refresh_models_button.pack(side="left", padx=5, pady=10)
        
        self.download_model_button = ctk.CTkButton(
            model_frame,
            text="Download",
            command=self.download_model,
            width=60,
            height=25
        )
        self.download_model_button.pack(side="left", padx=5, pady=10)
        
        # Prompt section
        prompt_frame = ctk.CTkFrame(self)
        prompt_frame.pack(fill="x", padx=10, pady=5)
        
        prompt_label = ctk.CTkLabel(prompt_frame, text="Prompt:", 
                                  font=ctk.CTkFont(size=12, weight="bold"))
        prompt_label.pack(pady=(10, 5))
        
        self.prompt_text = ctk.CTkTextbox(
            prompt_frame,
            height=80
        )
        self.prompt_text.pack(fill="x", padx=10, pady=5)
        
        # Context section
        context_frame = ctk.CTkFrame(self)
        context_frame.pack(fill="x", padx=10, pady=5)
        
        context_label = ctk.CTkLabel(context_frame, text="Context:", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        context_label.pack(pady=(10, 5))
        
        self.use_entire_table_var = tk.BooleanVar(value=False)
        self.use_entire_table_checkbox = ctk.CTkCheckBox(
            context_frame,
            text="Use entire table as context",
            variable=self.use_entire_table_var,
            command=self.update_context_info
        )
        self.use_entire_table_checkbox.pack(padx=10, pady=5)
        
        self.context_info_label = ctk.CTkLabel(
            context_frame,
            text="Context: Selected item only",
            font=ctk.CTkFont(size=10)
        )
        self.context_info_label.pack(padx=10, pady=(0, 10))
        
        # Preview section
        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(fill="x", padx=10, pady=5)
        
        preview_label = ctk.CTkLabel(preview_frame, text="AI Suggestions:", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(10, 5))
        
        self.preview_listbox = tk.Listbox(
            preview_frame,
            height=4,
            font=("Arial", 10)
        )
        self.preview_listbox.pack(fill="x", padx=10, pady=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Generate Preview",
            command=self.generate_preview,
            width=120,
            height=35,
            state="disabled"
        )
        self.preview_button.pack(side="left", padx=5)
        
        self.apply_ai_button = ctk.CTkButton(
            button_frame,
            text="Apply",
            command=self.apply_ai_suggestion,
            width=80,
            height=35,
            state="disabled"
        )
        self.apply_ai_button.pack(side="left", padx=5)
        
        # Load initial models and settings
        self.load_initial_settings()
    
    def load_initial_settings(self):
        """Load initial AI settings from config."""
        # Don't refresh models immediately - wait for main window to be fully initialized
        # Models will be refreshed when user clicks refresh button or when needed
        pass
    
    def refresh_models(self):
        """Refresh the list of available models."""
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status("Refreshing AI models...")
        
        # Run in a separate thread to avoid blocking UI
        def refresh_thread():
            if self.ollama_handler.is_ollama_running():
                self.available_models = self.ollama_handler.get_available_models()
                if self.available_models:
                    # Update UI in main thread
                    self.after(0, self.update_model_dropdown)
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.update_status(f"Found {len(self.available_models)} AI models")
                else:
                    self.after(0, lambda: self.update_model_dropdown(show_error=True))
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.update_status("No AI models found")
            else:
                self.after(0, lambda: self.update_model_dropdown(show_error=True))
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.update_status("Ollama service not running")
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def update_model_dropdown(self, show_error=False):
        """Update the model dropdown with available models."""
        if show_error or not self.available_models:
            self.model_dropdown.configure(values=["No models available"])
            self.model_dropdown.set("No models available")
            self.preview_button.configure(state="disabled")
        else:
            self.model_dropdown.configure(values=self.available_models)
            if self.available_models:
                self.model_dropdown.set(self.available_models[0])
                self.preview_button.configure(state="normal")
    
    def download_model(self):
        """Download a model dialog."""
        # Simple input dialog for model name
        dialog = ctk.CTkInputDialog(text="Enter model name to download:", title="Download Model")
        model_name = dialog.get_input()
        
        if model_name:
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Downloading model: {model_name}")
            
            # Run download in separate thread
            def download_thread():
                success = self.ollama_handler.pull_model(model_name)
                self.after(0, lambda: self.download_complete(success, model_name))
            
            threading.Thread(target=download_thread, daemon=True).start()
    
    def download_complete(self, success, model_name):
        """Handle download completion."""
        if success:
            self.refresh_models()
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Model '{model_name}' downloaded successfully")
        else:
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Failed to download model '{model_name}'")
            messagebox.showerror("Error", f"Failed to download model '{model_name}'")
    
    def update_context_info(self):
        """Update context information label."""
        if self.use_entire_table_var.get():
            self.context_info_label.configure(text="Context: Entire table")
        else:
            self.context_info_label.configure(text="Context: Selected item only")
    
    def generate_preview(self):
        """Generate AI preview suggestions."""
        if not self.selected_item or not self.available_models:
            return
        
        model_name = self.model_dropdown.get()
        prompt = self.prompt_text.get("1.0", "end-1c").strip()
        
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt")
            return
        
        if model_name == "No models available":
            messagebox.showwarning("Warning", "No AI models available")
            return
        
        # Save selected model to config
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            self.main_window.config_manager.save_selected_model(model_name)
        
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status("Generating AI suggestions...")
        
        # Disable button during generation
        self.preview_button.configure(state="disabled")
        
        # Run generation in separate thread
        def generate_thread():
            try:
                # Prepare context
                if self.use_entire_table_var.get():
                    context = self.get_entire_table_context()
                else:
                    context = self.get_selected_item_context()
                
                # Generate suggestions
                suggestions = self.ollama_handler.generate_erp_names(
                    prompt, context, model_name, 5
                )
                
                # Update UI in main thread
                self.after(0, lambda: self.update_preview_list(suggestions))
                
            except Exception as e:
                self.after(0, lambda: self.generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def get_selected_item_context(self):
        """Get context for selected item only."""
        if self.selected_item:
            return f"Current ERP name: {self.selected_item.get('ERP name', 'Unknown')}"
        return "No item selected"
    
    def get_entire_table_context(self):
        """Get context for entire table."""
        if hasattr(self.tree_view, 'data') and not self.tree_view.data.empty:
            erp_names = self.tree_view.data['ERP name'].dropna().unique()
            context = f"Available ERP names in table: {', '.join(erp_names[:10])}"  # Limit to first 10
            if len(erp_names) > 10:
                context += f" (and {len(erp_names) - 10} more)"
            return context
        return "No table data available"
    
    def update_preview_list(self, suggestions):
        """Update the preview listbox with suggestions."""
        self.preview_listbox.delete(0, tk.END)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                self.preview_listbox.insert(tk.END, f"{i}. {suggestion}")
            self.apply_ai_button.configure(state="normal")
            
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Generated {len(suggestions)} AI suggestions")
        else:
            self.preview_listbox.insert(tk.END, "No suggestions generated")
            self.apply_ai_button.configure(state="disabled")
            
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("No AI suggestions generated")
        
        self.preview_button.configure(state="normal")
    
    def generation_error(self, error_message):
        """Handle generation error."""
        self.preview_listbox.delete(0, tk.END)
        self.preview_listbox.insert(tk.END, f"Error: {error_message}")
        self.apply_ai_button.configure(state="disabled")
        self.preview_button.configure(state="normal")
        
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status("Error generating AI suggestions")
    
    def apply_ai_suggestion(self):
        """Apply selected AI suggestion to User ERP Name."""
        selection = self.preview_listbox.curselection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a suggestion to apply")
            return
        
        if not self.selected_row_id:
            messagebox.showwarning("Warning", "No item selected")
            return
        
        # Get the selected suggestion
        suggestion_text = self.preview_listbox.get(selection[0])
        # Remove numbering and clean up
        suggestion = suggestion_text.split('. ', 1)[-1] if '. ' in suggestion_text else suggestion_text
        
        # Apply to User ERP Name
        self.tree_view.update_user_erp_name(self.selected_row_id, suggestion)
        
        # Update the input field
        self.user_erp_name_entry.delete(0, tk.END)
        self.user_erp_name_entry.insert(0, suggestion)
        
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Applied AI suggestion: {suggestion}")
