"""
AI Editor for ERP Database Editor
Provides AI-powered editing functionality for selected ERP items.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from src.backend.ollama_handler import OllamaHandler
from src.backend.prompt_manager import PromptManager
from src.gui.prompt_dialog import PromptSelectionDialog
from src.gui.save_prompt_dialog import SavePromptDialog
from src.gui.model_manager_dialog import ModelManagerDialog


class AIEditor(ctk.CTkFrame):
    """AI editor panel for AI-powered editing of selected ERP items."""

    # Width constants for consistent UI sizing
    MODEL_LABEL_WIDTH = 60       # Width for model label
    MODEL_DROPDOWN_WIDTH = 150   # Width for model dropdown
    REFRESH_BUTTON_WIDTH = 50    # Width for refresh button
    MANAGE_BUTTON_WIDTH = 60     # Width for manage button
    PROMPT_BUTTON_WIDTH = 80     # Width for prompt tool button
    GENERATE_BUTTON_WIDTH = 80   # Width for generate button
    APPLY_SELECTED_WIDTH = 120   # Width for apply selected button
    APPLY_ENTIRE_WIDTH = 140     # Width for apply entire table button

    # Height constants for consistent UI sizing
    SMALL_BUTTON_HEIGHT = 25     # Height for small control buttons (Refresh, Manage, Prompt Tool)
    ACTION_BUTTON_HEIGHT = 30    # Height for action buttons (Generate, Apply Selected, Apply Entire)
    LISTBOX_HEIGHT = 6           # Height for results listbox
    SEPARATOR_HEIGHT = 2         # Height for separator lines

    def __init__(self, parent, tree_view, main_window=None):
        """Initialize the AI editor."""
        super().__init__(parent)

        self.tree_view = tree_view
        self.main_window = main_window
        self.selected_item = None
        self.selected_row_id = None

        # Initialize Ollama handler
        self.ollama_handler = OllamaHandler()
        self.available_models = []

        # Initialize prompt manager
        self.prompt_manager = PromptManager()

        # Processing control
        self.processing_thread = None
        self.should_stop_processing = False

        # Store selected prompt name and text
        self.selected_prompt = None
        self.selected_prompt_text = None

        # Panel will be sized by the tabview container

        # Create the AI editor interface
        self.setup_ai_editor()

    def setup_ai_editor(self):
        """Setup the AI editor components."""
        # Title
        title_label = ctk.CTkLabel(self, text="AI-Powered Editing", font=ctk.CTkFont(size=16, weight="bold"))
        title_label.pack(pady=(10, 10))

        # AI Settings subsection
        self.setup_ai_settings_section()

        # Separator
        separator = ctk.CTkFrame(self, height=self.SEPARATOR_HEIGHT)
        separator.pack(fill="x", padx=10, pady=10)

        # AI Results section
        self.setup_ai_results_section()

        # Initialize AI functionality after UI is set up
        self.main_window.root.after(1000, self.initialize_ai_functionality)  # Delay to ensure main window is fully loaded

    def setup_ai_settings_section(self):
        """Setup the AI settings section."""
        # AI Settings frame
        ai_settings_frame = ctk.CTkFrame(self)
        ai_settings_frame.pack(fill="x", padx=10, pady=5)

        ai_settings_label = ctk.CTkLabel(ai_settings_frame, text="AI Settings:",
                                       font=ctk.CTkFont(size=12, weight="bold"))
        ai_settings_label.pack(pady=(5, 3))

        # Model selection frame
        model_frame = ctk.CTkFrame(ai_settings_frame)
        model_frame.pack(fill="x", padx=10, pady=5)

        model_label = ctk.CTkLabel(model_frame, text="Model:", width=self.MODEL_LABEL_WIDTH)
        model_label.pack(side="left", padx=(10, 5), pady=5)

        self.model_dropdown = ctk.CTkOptionMenu(
            model_frame,
            values=["No models available"],
            width=self.MODEL_DROPDOWN_WIDTH,
            command=self.on_model_selection_change
        )
        self.model_dropdown.pack(side="left", padx=5, pady=5)

        # Model control buttons
        self.refresh_models_button = ctk.CTkButton(
            model_frame,
            text="Refresh",
            command=self.refresh_models,
            width=self.REFRESH_BUTTON_WIDTH,
            height=self.SMALL_BUTTON_HEIGHT
        )
        self.refresh_models_button.pack(side="left", padx=5, pady=5)

        self.manage_models_button = ctk.CTkButton(
            model_frame,
            text="Manage",
            command=self.open_model_manager,
            width=self.MANAGE_BUTTON_WIDTH,
            height=self.SMALL_BUTTON_HEIGHT
        )
        self.manage_models_button.pack(side="left", padx=5, pady=5)

        # Prompt Tool button in AI Settings
        self.prompt_tool_button = ctk.CTkButton(
            model_frame,
            text="Prompt Tool",
            command=self.select_prompt,
            width=self.PROMPT_BUTTON_WIDTH,
            height=self.SMALL_BUTTON_HEIGHT
        )
        self.prompt_tool_button.pack(side="left", padx=5, pady=5)

        # Prompt status label
        self.prompt_status_label = ctk.CTkLabel(
            model_frame,
            text="No prompt loaded",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.prompt_status_label.pack(side="left", padx=(10, 5), pady=5)

    def setup_ai_results_section(self):
        """Setup the AI results section."""
        # Preview section
        preview_frame = ctk.CTkFrame(self)
        preview_frame.pack(fill="x", padx=10, pady=5)

        preview_label = ctk.CTkLabel(preview_frame, text="AI Results:",
                                   font=ctk.CTkFont(size=12, weight="bold"))
        preview_label.pack(pady=(5, 3))

        self.preview_listbox = tk.Listbox(
            preview_frame,
            height=self.LISTBOX_HEIGHT,  # Shows 5 results
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
            width=self.GENERATE_BUTTON_WIDTH,
            height=self.ACTION_BUTTON_HEIGHT,
            state="normal"
        )
        self.preview_button.pack(side="left", padx=5)

        self.apply_to_selected_button = ctk.CTkButton(
            button_frame,
            text="Process Selected",
            command=self.apply_ai_to_selected,
            width=self.APPLY_SELECTED_WIDTH,
            height=self.ACTION_BUTTON_HEIGHT,
            state="disabled"
        )
        self.apply_to_selected_button.pack(side="left", padx=5)

        self.apply_to_entire_table_button = ctk.CTkButton(
            button_frame,
            text="Process entire table",
            command=self.apply_ai_to_entire_table,
            width=self.APPLY_ENTIRE_WIDTH,
            height=self.ACTION_BUTTON_HEIGHT,
            state="disabled"
        )
        self.apply_to_entire_table_button.pack(side="left", padx=5)

    def initialize_ai_functionality(self):
        """Initialize AI functionality after the main window is fully loaded."""
        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.refresh_models()
            # Load previously selected model from config
            self.load_selected_model_from_config()
            # Load previously selected prompt from config
            self.load_selected_prompt_from_config()

    def load_initial_settings(self):
        """Load initial AI settings from config."""
        # Don't refresh models immediately - wait for main window to be fully initialized
        # Models will be refreshed when user clicks refresh button or when needed
        pass


    def load_selected_model_from_config(self):
        """Load previously selected model from config."""
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            config_manager = self.main_window.config_manager
            selected_model = config_manager.get_selected_model()

            if selected_model and selected_model in self.available_models:
                self.model_dropdown.set(selected_model)
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.update_status(f"Loaded AI model: {selected_model}")

    def load_selected_prompt_from_config(self):
        """Load previously selected prompt from config."""
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            config_manager = self.main_window.config_manager
            selected_prompt = config_manager.get_selected_prompt()

            if selected_prompt:
                self.selected_prompt = selected_prompt
                # Also load the prompt text
                self.selected_prompt_text = config_manager.get_selected_prompt_text()
                # Update the prompt status label to show that a saved prompt was loaded
                self.prompt_status_label.configure(
                    text=f"Prompt: {selected_prompt}",
                    text_color="green"
                )
                if self.main_window and hasattr(self.main_window, 'status_label'):
                    self.main_window.update_status("Loaded saved AI prompt")

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
                    # Load previously selected model after models are loaded
                    self.main_window.root.after(0, self.load_selected_model_from_config)
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

        # Update save view button state when model selection changes
        if self.main_window and hasattr(self.main_window, 'update_save_view_button_state'):
            self.main_window.root.after(0, self.main_window.update_save_view_button_state)

    def open_model_manager(self):
        """Open the model manager dialog."""
        try:
            dialog = ModelManagerDialog(self.main_window.root, self.main_window)
            # The dialog will handle its own lifecycle
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open model manager: {str(e)}")
            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("Error opening model manager")

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
            self.after(2000, self.generate_preview)  # Retry after 2 seconds
            return

        model_name = self.model_dropdown.get()
        # Use selected prompt text if available, otherwise use default
        if self.selected_prompt_text:
            prompt = self.selected_prompt_text
        else:
            prompt = "Generate a better ERP name for this item based on its category and specifications."

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

                # Get model parameters
                model_parameters = None
                if self.main_window and hasattr(self.main_window, 'config_manager'):
                    config_manager = self.main_window.config_manager
                    model_parameters = config_manager.get_model_parameters(model_name)

                # Generate suggestions
                suggestions = self.ollama_handler.generate_erp_names(
                    prompt, context, model_name, 5, model_parameters
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
            erp_name = self.selected_item.get('ERP name', 'Unknown')
            category = self.selected_item.get('Article Category', 'Unknown')
            subcategory = self.selected_item.get('Article Subcategory', 'Unknown')
            sublevel = self.selected_item.get('Article Sublevel', 'Unknown')
            return f"Current ERP name: {erp_name}, Category: {category}, Subcategory: {subcategory}, Sublevel: {sublevel}"

        # Check for multiple selected items
        if hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items:
            contexts = []
            for item_data, row_id in self.tree_view.selected_items:
                erp_name = item_data.get('ERP name', 'Unknown')
                category = item_data.get('Article Category', 'Unknown')
                subcategory = item_data.get('Article Subcategory', 'Unknown')
                sublevel = item_data.get('Article Sublevel', 'Unknown')
                contexts.append(f"ERP: {erp_name}, Cat: {category}, Sub: {subcategory}, Level: {sublevel}")

            if len(contexts) == 1:
                return f"Current item: {contexts[0]}"
            else:
                return f"Selected items: {'; '.join(contexts)}"

        return "No item selected"

    def update_preview_list(self, suggestions):
        """Update the preview listbox with suggestions."""
        self.preview_listbox.delete(0, tk.END)

        if suggestions:
            for i, suggestion in enumerate(suggestions, 1):
                self.preview_listbox.insert(tk.END, f"{i}. {suggestion}")

            # Enable "Process Selected" button if we have selected items
            if hasattr(self.tree_view, 'selected_items') and self.tree_view.selected_items:
                self.apply_to_selected_button.configure(state="normal")

            # Enable "Process entire table" button if we have data
            if hasattr(self.tree_view, 'data') and not self.tree_view.data.empty:
                self.apply_to_entire_table_button.configure(state="normal")

            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status(f"Generated {len(suggestions)} AI suggestions")
        else:
            self.preview_listbox.insert(tk.END, "No suggestions generated")
            self.apply_to_selected_button.configure(state="disabled")
            self.apply_to_entire_table_button.configure(state="disabled")

            if self.main_window and hasattr(self.main_window, 'status_label'):
                self.main_window.update_status("No AI suggestions generated")

        self.preview_button.configure(state="normal")

    def generation_error(self, error_message):
        """Handle generation error."""
        self.preview_listbox.delete(0, tk.END)
        self.preview_listbox.insert(tk.END, f"Error: {error_message}")
        self.apply_to_selected_button.configure(state="disabled")
        self.apply_to_entire_table_button.configure(state="disabled")
        self.preview_button.configure(state="normal")

        if self.main_window and hasattr(self.main_window, 'status_label'):
            self.main_window.update_status("Error generating AI suggestions")

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
        # Use selected prompt text if available, otherwise use default
        if self.selected_prompt_text:
            prompt = self.selected_prompt_text
        else:
            prompt = "Generate a better ERP name for this item based on its category and specifications."
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
                        # Prepare context for this specific item with all required fields
                        erp_name = item_data.get('ERP name', 'Unknown')
                        category = item_data.get('Article Category', 'Unknown')
                        subcategory = item_data.get('Article Subcategory', 'Unknown')
                        sublevel = item_data.get('Article Sublevel', 'Unknown')

                        context = f"Current ERP name: {erp_name}, Category: {category}, Subcategory: {subcategory}, Sublevel: {sublevel}"

                        # Get model parameters
                        model_parameters = None
                        if self.main_window and hasattr(self.main_window, 'config_manager'):
                            config_manager = self.main_window.config_manager
                            model_parameters = config_manager.get_model_parameters(model_name)

                        # Generate suggestion for this item
                        suggestions = self.ollama_handler.generate_erp_names(
                            prompt, context, model_name, 1, model_parameters
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
            text="Process entire table",
            state="normal"
        )
        self.apply_to_selected_button.configure(
            text="Process Selected",
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
        # Use selected prompt text if available, otherwise use default
        if self.selected_prompt_text:
            prompt = self.selected_prompt_text
        else:
            prompt = "Generate a better ERP name for this item based on its category and specifications."
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
                        row_id = f"{row.get('ERP name', '')}{delimiter}{row.get('Article Category', '')}{delimiter}{row.get('Article Subcategory', '')}{delimiter}{row.get('Article Sublevel', '')}"

                        # Prepare context for this specific item with all required fields
                        erp_name = row.get('ERP name', 'Unknown')
                        category = row.get('Article Category', 'Unknown')
                        subcategory = row.get('Article Subcategory', 'Unknown')
                        sublevel = row.get('Article Sublevel', 'Unknown')

                        context = f"Current ERP name: {erp_name}, Category: {category}, Subcategory: {subcategory}, Sublevel: {sublevel}"

                        # Get model parameters
                        model_parameters = None
                        if self.main_window and hasattr(self.main_window, 'config_manager'):
                            config_manager = self.main_window.config_manager
                            model_parameters = config_manager.get_model_parameters(model_name)

                        # Generate suggestion for this item
                        suggestions = self.ollama_handler.generate_erp_names(
                            prompt, context, model_name, 1, model_parameters
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
            text="Process entire table",
            state="normal"
        )
        self.apply_to_selected_button.configure(
            text="Process Selected",
            state="normal"
        )

        # Reset processing state
        self.processing_thread = None
        self.should_stop_processing = False

    def select_prompt(self):
        """Open the prompt selection dialog."""
        # Open prompt selection dialog
        select_dialog = PromptSelectionDialog(
            self.main_window.root,
            on_prompt_selected=self.on_prompt_selected
        )

    def on_prompt_selected(self, prompt_name: str, prompt_text: str):
        """Callback when a prompt is selected.

        Args:
            prompt_name: The name/key of the selected prompt
            prompt_text: The selected prompt text
        """
        # Store both the prompt key and text for use in AI operations
        self.selected_prompt = prompt_name
        self.selected_prompt_text = prompt_text

        # Update the status label to show the prompt name
        self.prompt_status_label.configure(
            text=f"Prompt: {prompt_name}",
            text_color="green"
        )

        # Show status message
        if self.main_window and hasattr(self.main_window, 'update_status'):
            self.main_window.update_status(f"Prompt '{prompt_name}' loaded successfully")

        # Update save view button state when prompt selection changes
        if self.main_window and hasattr(self.main_window, 'update_save_view_button_state'):
            self.main_window.update_save_view_button_state()

    def on_model_selection_change(self, selected_model):
        """Handle model selection change."""
        # Update save view button state when model selection changes
        if self.main_window and hasattr(self.main_window, 'update_save_view_button_state'):
            self.main_window.update_save_view_button_state()

    def set_selected_item(self, item_data, row_id):
        """Set the selected item."""
        self.selected_item = item_data
        self.selected_row_id = row_id
