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
        
        # Processing control
        self.processing_thread = None
        self.should_stop_processing = False
        
        # Configure panel size
        self.configure(width=700)
        
        # Create the edit panel
        self.setup_edit_panel()
        
    def setup_edit_panel(self):
        """Setup the edit panel components."""
        # Title
        title_label = ctk.CTkLabel(self, text="Edit Selected Item", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(5, 10))
        
        # User ERP Name section
        self.setup_user_erp_name_section()
        
        # Separator
        separator1 = ctk.CTkFrame(self, height=2)
        separator1.pack(fill="x", padx=10, pady=10)
        
        # Reassignment section
        self.setup_reassignment_section()
        
        # Separator
        separator2 = ctk.CTkFrame(self, height=2)
        separator2.pack(fill="x", padx=10, pady=10)
        
        # AI Editing section
        self.setup_ai_editing_section()
        
    def setup_user_erp_name_section(self):
        """Setup the User ERP Name editing section."""
        # Input field and buttons frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=(0, 5))
        
        # Input field
        self.user_erp_name_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter User ERP Name...",
            width=400,
            height=35
        )
        self.user_erp_name_entry.pack(side="left", padx=(0, 10))
        
        # Update button
        self.update_name_button = ctk.CTkButton(
            input_frame,
            text="Update",
            command=self.update_user_erp_name,
            width=80,
            height=30,
            state="disabled"
        )
        self.update_name_button.pack(side="left", padx=(0, 5))
        
        # Reset button
        self.reset_name_button = ctk.CTkButton(
            input_frame,
            text="Reset",
            command=self.reset_user_erp_name,
            width=60,
            height=30,
            state="disabled"
        )
        self.reset_name_button.pack(side="left")
        
    def setup_reassignment_section(self):
        """Setup the reassignment section."""
        # Main container frame for two-column layout
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="x", padx=10, pady=5)
        
        # Left column for dropdowns
        left_column = ctk.CTkFrame(main_frame)
        left_column.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)
        
        # Category dropdown
        category_frame = ctk.CTkFrame(left_column)
        category_frame.pack(fill="x", pady=2)
        
        category_label = ctk.CTkLabel(category_frame, text="Category:", width=100)
        category_label.pack(side="left", padx=(10, 5), pady=5)
        
        self.category_dropdown = ctk.CTkOptionMenu(
            category_frame,
            values=["Select Category..."],
            command=self.on_category_change,
            width=200
        )
        self.category_dropdown.pack(side="left", padx=5, pady=5)
        
        # Subcategory dropdown
        subcategory_frame = ctk.CTkFrame(left_column)
        subcategory_frame.pack(fill="x", pady=2)
        
        subcategory_label = ctk.CTkLabel(subcategory_frame, text="Subcategory:", width=100)
        subcategory_label.pack(side="left", padx=(10, 5), pady=5)
        
        self.subcategory_dropdown = ctk.CTkOptionMenu(
            subcategory_frame,
            values=["Select Subcategory..."],
            command=self.on_subcategory_change,
            width=200
        )
        self.subcategory_dropdown.pack(side="left", padx=5, pady=5)
        
        # Sublevel dropdown
        sublevel_frame = ctk.CTkFrame(left_column)
        sublevel_frame.pack(fill="x", pady=2)
        
        sublevel_label = ctk.CTkLabel(sublevel_frame, text="Sublevel:", width=100)
        sublevel_label.pack(side="left", padx=(10, 5), pady=5)
        
        self.sublevel_dropdown = ctk.CTkOptionMenu(
            sublevel_frame,
            values=["Select Sublevel..."],
            width=200
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
            width=100,
            height=90,  # Increased height to span the three dropdown rows
            state="disabled"
        )
        self.reassign_button.pack(pady=5)
        
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
            
            # Enable buttons when item is selected
            self.update_name_button.configure(state="normal")
            self.reset_name_button.configure(state="normal")
            
            # Set the dropdowns to current item's category/subcategory/sublevel
            current_category = item_data.get('Article Category', '')
            current_subcategory = item_data.get('Article Subcategory', '')
            current_sublevel = item_data.get('Article Sublevel ', '')
            
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
            
            # Disable buttons when no item is selected
            self.update_name_button.configure(state="disabled")
            self.reset_name_button.configure(state="disabled")
            self.reassign_button.configure(state="disabled")
            self.apply_to_selected_button.configure(state="disabled")
            self.apply_to_entire_table_button.configure(state="disabled")
            
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
        # AI Settings subsection
        ai_settings_frame = ctk.CTkFrame(self)
        ai_settings_frame.pack(fill="x", padx=10, pady=5)
        
        ai_settings_label = ctk.CTkLabel(ai_settings_frame, text="AI Settings:", 
                                       font=ctk.CTkFont(size=12, weight="bold"))
        ai_settings_label.pack(pady=(5, 3))
        
        # Model selection frame
        model_frame = ctk.CTkFrame(ai_settings_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        
        model_label = ctk.CTkLabel(model_frame, text="Model:", width=60)
        model_label.pack(side="left", padx=(10, 5), pady=5)
        
        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["No models available"],
            width=150
        )
        self.model_dropdown.pack(side="left", padx=5, pady=5)
        
        # Model control buttons
        self.refresh_models_button = ctk.CTkButton(
            model_frame,
            text="Refresh",
            command=self.refresh_models,
            width=50,
            height=25
        )
        self.refresh_models_button.pack(side="left", padx=5, pady=5)
        
        self.download_model_button = ctk.CTkButton(
            model_frame,
            text="Download",
            command=self.download_model,
            width=60,
            height=25
        )
        self.download_model_button.pack(side="left", padx=5, pady=5)
        
        # Prompt section
        prompt_frame = ctk.CTkFrame(self)
        prompt_frame.pack(fill="x", padx=10, pady=5)
        
        prompt_label = ctk.CTkLabel(prompt_frame, text="Prompt:", 
                                  font=ctk.CTkFont(size=12, weight="bold"))
        prompt_label.pack(pady=(5, 3))
        
        self.prompt_text = ctk.CTkTextbox(
            prompt_frame,
            height=80
        )
        self.prompt_text.pack(fill="x", padx=10, pady=5)
        
        
        # Preview section
        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(fill="x", padx=10, pady=5)
        
        preview_label = ctk.CTkLabel(preview_frame, text="AI Results:", 
                                   font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(5, 3))
        
        self.preview_listbox = tk.Listbox(
            preview_frame,
            height=6,  # Increased height for 5 results
            font=("Arial", 10)
        )
        self.preview_listbox.pack(fill="x", padx=10, pady=5)
        
        # Action buttons
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        self.preview_button = ctk.CTkButton(
            button_frame,
            text="Generate",
            command=self.generate_preview,
            width=80,
            height=30,
            state="normal"
        )
        self.preview_button.pack(side="left", padx=5)
        
        self.apply_ai_button = ctk.CTkButton(
            button_frame,
            text="Apply",
            command=self.apply_ai_suggestion,
            width=60,
            height=30,
            state="disabled"
        )
        self.apply_ai_button.pack(side="left", padx=5)
        
        self.apply_to_selected_button = ctk.CTkButton(
            button_frame,
            text="Apply to selected",
            command=self.apply_ai_to_selected,
            width=120,
            height=30,
            state="disabled"
        )
        self.apply_to_selected_button.pack(side="left", padx=5)
        
        self.apply_to_entire_table_button = ctk.CTkButton(
            button_frame,
            text="Apply to entire table",
            command=self.apply_ai_to_entire_table,
            width=140,
            height=30,
            state="disabled"
        )
        self.apply_to_entire_table_button.pack(side="left", padx=5)
        
        # Load initial models and settings
        self.load_initial_settings()
    
    def load_initial_settings(self):
        """Load initial AI settings from config."""
        # Don't refresh models immediately - wait for main window to be fully initialized
        # Models will be refreshed when user clicks refresh button or when needed
        pass
    
    def refresh_models_on_startup(self):
        """Refresh AI models after main window is fully initialized."""
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.refresh_models()
            # Load previously selected model from config
            self.load_selected_model_from_config()
    
    def load_selected_model_from_config(self):
        """Load previously selected model from config."""
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            config_manager = self.main_window.config_manager
            selected_model = config_manager.get_selected_model()
            
            if selected_model and selected_model in self.available_models:
                self.model_dropdown.set(selected_model)
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.update_status(f"Loaded AI model: {selected_model}")
    
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
                    self.main_window.root.after(0, self.update_model_dropdown)
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.update_status(f"Found {len(self.available_models)} AI models")
                else:
                    self.main_window.root.after(0, lambda: self.update_model_dropdown(show_error=True))
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.update_status("No AI models found")
            else:
                self.main_window.root.after(0, lambda: self.update_model_dropdown(show_error=True))
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
                self.main_window.root.after(0, lambda: self.download_complete(success, model_name))
            
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
    
    
    def generate_preview(self):
        """Generate AI preview suggestions."""
        # Check if we have any selected items (either single or multiple)
        if not self.selected_item and not (hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items):
            messagebox.showwarning("Warning", "Please select an item in the tree view first")
            return
        
        # If no models are available, try to refresh them
        if not self.available_models:
            messagebox.showinfo("Info", "Loading AI models...")
            self.refresh_models()
            # Wait a moment for models to load
            self.main_window.root.after(2000, self.generate_preview)  # Retry after 2 seconds
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
                # Prepare context (always use selected item context)
                context = self.get_selected_item_context()
                
                # Generate suggestions
                suggestions = self.ollama_handler.generate_erp_names(
                    prompt, context, model_name, 5
                )
                
                # Update UI in main thread
                self.main_window.root.after(0, lambda: self.update_preview_list(suggestions))
                
            except Exception as e:
                self.main_window.root.after(0, lambda: self.generation_error(str(e)))
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def get_selected_item_context(self):
        """Get context for selected item(s) only."""
        # Check for single selected item
        if self.selected_item:
            return f"Current ERP name: {self.selected_item.get('ERP name', 'Unknown')}"
        
        # Check for multiple selected items
        if hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items:
            erp_names = []
            for item_data, row_id in self.tree_view.selected_items:
                erp_name = item_data.get('ERP name', 'Unknown')
                erp_names.append(erp_name)
            
            if len(erp_names) == 1:
                return f"Current ERP name: {erp_names[0]}"
            else:
                return f"Selected ERP names: {', '.join(erp_names)}"
        
        return "No item selected"
    
    
    def update_preview_list(self, suggestions):
        """Update the preview listbox with suggestions."""
        self.preview_listbox.delete(0, tk.END)
        
        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                self.preview_listbox.insert(tk.END, f"{i}. {suggestion}")
            self.apply_ai_button.configure(state="normal")
            
            # Enable "Apply to selected" button if we have selected items
            if hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items:
                self.apply_to_selected_button.configure(state="normal")
            
            # Enable "Apply to entire table" button if we have data
            if hasattr(self.tree_view, 'data') and not self.tree_view.data.empty:
                self.apply_to_entire_table_button.configure(state="normal")
            
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Generated {len(suggestions)} AI suggestions")
        else:
            self.preview_listbox.insert(tk.END, "No suggestions generated")
            self.apply_ai_button.configure(state="disabled")
            self.apply_to_selected_button.configure(state="disabled")
            self.apply_to_entire_table_button.configure(state="disabled")
            
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("No AI suggestions generated")
        
        self.preview_button.configure(state="normal")
    
    def generation_error(self, error_message):
        """Handle generation error."""
        self.preview_listbox.delete(0, tk.END)
        self.preview_listbox.insert(tk.END, f"Error: {error_message}")
        self.apply_ai_button.configure(state="disabled")
        self.apply_to_selected_button.configure(state="disabled")
        self.apply_to_entire_table_button.configure(state="disabled")
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
        
        # Show confirmation dialog
        current_name = self.user_erp_name_entry.get()
        if current_name:
            response = messagebox.askyesno(
                "Confirm AI Application", 
                f"Current User ERP Name: '{current_name}'\n\nAI Suggestion: '{suggestion}'\n\nDo you want to apply this AI suggestion?"
            )
        else:
            response = messagebox.askyesno(
                "Confirm AI Application", 
                f"AI Suggestion: '{suggestion}'\n\nDo you want to apply this AI suggestion?"
            )
        
        if response:
            # Apply to User ERP Name
            self.tree_view.update_user_erp_name(self.selected_row_id, suggestion)
            
            # Update the input field
            self.user_erp_name_entry.delete(0, tk.END)
            self.user_erp_name_entry.insert(0, suggestion)
            
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Applied AI suggestion: {suggestion}")
        else:
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("AI suggestion application cancelled")

    def apply_ai_to_selected(self):
        """Apply AI prompt to all selected items individually."""
        # Check if we're already processing - if so, stop processing
        if self.processing_thread and self.processing_thread.is_alive():
            self.stop_processing()
            return
        
        # Check if we have selected items
        if not (hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items):
            messagebox.showwarning("Warning", "Please select items in the tree view first")
            return
        
        # Check if we have a prompt
        prompt = self.prompt_text.get("1.0", "end-1c").strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt first")
            return
        
        # Check if we have models available
        if not self.available_models:
            messagebox.showwarning("Warning", "No AI models available. Please refresh models.")
            return
        
        # Show confirmation dialog
        num_items = len(self.tree_view.selected_items)
        response = messagebox.askyesno(
            "Confirm AI Application to Selected Items", 
            f"Apply AI prompt to {num_items} selected items?\n\nThis will generate individual suggestions for each item.\n\nPrompt: '{prompt}'\n\nYou can stop processing at any time by clicking the button again."
        )
        
        if not response:
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("AI application to selected items cancelled")
            return
        
        # Start processing for selected items
        self.start_processing_selected(prompt, num_items)
    
    def start_processing_selected(self, prompt, num_items):
        """Start the AI processing for selected items."""
        # Reset stop flag
        self.should_stop_processing = False
        
        # Get model name
        model_name = self.model_dropdown.get()
        
        # Update button to show stop functionality
        self.apply_to_selected_button.configure(
            text="Stop processing",
            state="normal"
        )
        
        # Update status
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Processing AI prompt for {num_items} selected items... Click 'Stop processing' to cancel.")
        
        # Run in separate thread
        def apply_thread():
            try:
                successful_applications = 0
                
                for i, (item_data, row_id) in enumerate(self.tree_view.selected_items):
                    # Check if we should stop processing
                    if self.should_stop_processing:
                        if self.main_window and hasattr(self.main_window, 'status_label'):
                            self.main_window.root.after(0, lambda: 
                                self.main_window.update_status(f"Processing stopped by user. Processed {successful_applications}/{num_items} items."))
                        break
                    
                    try:
                        # Prepare context for this specific item
                        context = f"Current ERP name: {item_data.get('ERP name', 'Unknown')}"
                        
                        # Generate suggestion for this item
                        suggestions = self.ollama_handler.generate_erp_names(
                            prompt, context, model_name, 1
                        )
                        
                        if suggestions and not self.should_stop_processing:
                            # Use the first (and only) suggestion
                            suggestion = suggestions[0].split('. ', 1)[-1] if '. ' in suggestions[0] else suggestions[0]
                            
                            # Apply to User ERP Name
                            self.tree_view.update_user_erp_name(row_id, suggestion)
                            successful_applications += 1
                        
                        # Update status for this item (only if not stopped)
                        if not self.should_stop_processing and self.main_window and hasattr(self.main_window, 'status_label'):
                            self.main_window.root.after(0, lambda i=i+1, total=num_items: 
                                self.main_window.update_status(f"Processing item {i}/{total}... (Click 'Stop processing' to cancel)"))
                        
                    except Exception as e:
                        print(f"Error processing item {i+1}: {e}")
                        continue
                
                # Update final status (only if not stopped)
                if not self.should_stop_processing:
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.root.after(0, lambda: 
                            self.main_window.update_status(f"Applied AI prompt to {successful_applications}/{num_items} items successfully"))
                else:
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.root.after(0, lambda: 
                            self.main_window.update_status(f"Processing cancelled. Applied AI prompt to {successful_applications}/{num_items} items."))
                
            except Exception as e:
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.root.after(0, lambda: 
                        self.main_window.update_status(f"Error applying AI prompt: {str(e)}"))
            
            finally:
                # Reset button state
                self.main_window.root.after(0, lambda: self.reset_selected_processing_button())
        
        # Store the thread reference
        self.processing_thread = threading.Thread(target=apply_thread, daemon=True)
        self.processing_thread.start()
    
    def reset_selected_processing_button(self):
        """Reset the processing buttons to their normal state."""
        self.apply_to_entire_table_button.configure(
            text="Apply to entire table",
            state="normal"
        )
        self.apply_to_selected_button.configure(
            text="Apply to selected",
            state="normal"
        )
        
        # Reset processing state
        self.processing_thread = None
        self.should_stop_processing = False

    def apply_ai_to_entire_table(self):
        """Apply AI prompt to all items in the table."""
        # Check if we're already processing - if so, stop processing
        if self.processing_thread and self.processing_thread.is_alive():
            self.stop_processing()
            return
        
        # Check if we have a prompt
        prompt = self.prompt_text.get("1.0", "end-1c").strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt first")
            return
        
        # Check if we have models available
        if not self.available_models:
            messagebox.showwarning("Warning", "No AI models available. Please refresh models.")
            return
        
        # Check if we have data
        if not hasattr(self.tree_view, 'data') or self.tree_view.data.empty:
            messagebox.showwarning("Warning", "No data available")
            return
        
        # Count total items
        total_items = len(self.tree_view.data)
        
        # Show confirmation dialog
        response = messagebox.askyesno(
            "Confirm AI Application to Entire Table", 
            f"Apply AI prompt to all {total_items} items in the table?\n\nThis will generate individual suggestions for each item.\n\nPrompt: '{prompt}'\n\nThis may take a while...\n\nYou can stop processing at any time by clicking the button again."
        )
        
        if not response:
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("AI application to entire table cancelled")
            return
        
        # Start processing
        self.start_processing(prompt, total_items)
    
    def start_processing(self, prompt, total_items):
        """Start the AI processing for entire table."""
        # Reset stop flag
        self.should_stop_processing = False
        
        # Get model name
        model_name = self.model_dropdown.get()
        
        # Update button to show stop functionality
        self.apply_to_entire_table_button.configure(
            text="Stop processing",
            state="normal"
        )
        
        # Update status
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status(f"Processing AI prompt for {total_items} items... Click 'Stop processing' to cancel.")
        
        # Run in separate thread
        def apply_thread():
            try:
                successful_applications = 0
                
                for i, (_, row) in enumerate(self.tree_view.data.iterrows()):
                    # Check if we should stop processing
                    if self.should_stop_processing:
                        if self.main_window and hasattr(self.main_window, 'status_label'):
                            self.main_window.root.after(0, lambda: 
                                self.main_window.update_status(f"Processing stopped by user. Processed {successful_applications}/{total_items} items."))
                        break
                    
                    try:
                        # Get row ID for this item
                        delimiter = "◆◆◆"
                        row_id = f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{row.get('Article Sublevel ', '')}"
                        
                        # Prepare context for this specific item
                        context = f"Current ERP name: {row.get('ERP name', 'Unknown')}"
                        
                        # Generate suggestion for this item
                        suggestions = self.ollama_handler.generate_erp_names(
                            prompt, context, model_name, 1
                        )
                        
                        if suggestions and not self.should_stop_processing:
                            # Use the first (and only) suggestion
                            suggestion = suggestions[0].split('. ', 1)[-1] if '. ' in suggestions[0] else suggestions[0]
                            
                            # Apply to User ERP Name
                            self.tree_view.update_user_erp_name(row_id, suggestion)
                            successful_applications += 1
                        
                        # Update status for this item (only if not stopped)
                        if not self.should_stop_processing and self.main_window and hasattr(self.main_window, 'status_label'):
                            self.main_window.root.after(0, lambda i=i+1, total=total_items: 
                                self.main_window.update_status(f"Processing item {i}/{total}... (Click 'Stop processing' to cancel)"))
                        
                    except Exception as e:
                        print(f"Error processing item {i+1}: {e}")
                        continue
                
                # Update final status (only if not stopped)
                if not self.should_stop_processing:
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.root.after(0, lambda: 
                            self.main_window.update_status(f"Applied AI prompt to {successful_applications}/{total_items} items successfully"))
                else:
                    if self.main_window and hasattr(self.main_window, 'status_label'):
                        self.main_window.root.after(0, lambda: 
                            self.main_window.update_status(f"Processing cancelled. Applied AI prompt to {successful_applications}/{total_items} items."))
                
            except Exception as e:
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.root.after(0, lambda: 
                        self.main_window.update_status(f"Error applying AI prompt: {str(e)}"))
            
            finally:
                # Reset button state
                self.main_window.root.after(0, lambda: self.reset_processing_button())
        
        # Store the thread reference
        self.processing_thread = threading.Thread(target=apply_thread, daemon=True)
        self.processing_thread.start()
    
    def stop_processing(self):
        """Stop the current AI processing."""
        self.should_stop_processing = True
        
        # Update buttons immediately to show we're stopping
        self.apply_to_entire_table_button.configure(
            text="Stopping...",
            state="disabled"
        )
        self.apply_to_selected_button.configure(
            text="Stopping...",
            state="disabled"
        )
        
        # Update status
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status("Stopping AI processing...")
    
    def reset_processing_button(self):
        """Reset the processing buttons to their normal state."""
        self.apply_to_entire_table_button.configure(
            text="Apply to entire table",
            state="normal"
        )
        self.apply_to_selected_button.configure(
            text="Apply to selected",
            state="normal"
        )
        
        # Reset processing state
        self.processing_thread = None
        self.should_stop_processing = False

    def update_apply_to_selected_button_state(self):
        """Update the state of the Apply to selected button based on current selection and AI results."""
        # Enable if we have selected items and AI suggestions are available
        if (hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items and 
            self.preview_listbox.size() > 0 and 
            not self.preview_listbox.get(0, tk.END)[0].startswith("No suggestions") and
            not self.preview_listbox.get(0, tk.END)[0].startswith("Error:")):
            self.apply_to_selected_button.configure(state="normal")
        else:
            self.apply_to_selected_button.configure(state="disabled")
