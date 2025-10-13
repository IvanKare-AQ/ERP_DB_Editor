"""
Model Manager Dialog for ERP Database Editor
Provides functionality to manage AI models (download, remove, and configure parameters).
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
from src.backend.ollama_handler import OllamaHandler


class ModelManagerDialog:
    """Dialog for managing AI models."""

    # Width constants for consistent UI sizing
    REMOVE_BUTTON_WIDTH = 120    # Width for remove button
    REFRESH_BUTTON_WIDTH = 80    # Width for refresh button
    MODEL_INPUT_WIDTH = 300      # Width for model name input
    DOWNLOAD_BUTTON_WIDTH = 100  # Width for download button
    SAVE_BUTTON_WIDTH = 140      # Width for save parameters button
    CHECKBOX_WIDTH = 20          # Width for checkboxes
    LABEL_WIDTH = 100            # Width for labels
    ENTRY_WIDTH = 180            # Width for parameter entries (text)
    SLIDER_ENTRY_WIDTH = 70      # Width for slider value entries
    SLIDER_WIDTH = 120           # Width for parameter sliders
    OPTION_MENU_WIDTH = 100      # Width for option menus

    # Height constants for consistent UI sizing
    BUTTON_HEIGHT = 35           # Height for all buttons
    CHECKBOX_HEIGHT = 20         # Height for checkboxes
    ENTRY_HEIGHT = 35            # Height for entries

    def __init__(self, parent, main_window=None):
        """Initialize the model manager dialog."""
        self.parent = parent
        self.main_window = main_window
        self.ollama_handler = OllamaHandler()
        self.available_models = []
        self.selected_model = None
        self.model_parameters = {}
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Manage AI Models")
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.center_dialog()
        
        # Setup the dialog
        self.setup_dialog()
        
        # Load initial models
        self.load_models()
    
    def center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_reqwidth()
        dialog_height = self.dialog.winfo_reqheight()
        
        # Calculate position to center dialog
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def setup_dialog(self):
        """Setup the dialog components."""
        # Main container with horizontal layout
        main_frame = ctk.CTkFrame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="AI Model Manager",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Create horizontal layout
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True)
        
        # Left panel for model list and actions
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)
        
        # Right panel for model parameters
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)
        
        # Setup left panel
        self.setup_left_panel(left_panel)
        
        # Setup right panel
        self.setup_right_panel(right_panel)
        
        # Status bar
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Loading models...",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(10, 0))
    
    def setup_left_panel(self, parent):
        """Setup the left panel with model list and actions."""
        # Models list title
        models_title = ctk.CTkLabel(
            parent,
            text="Available Models:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        models_title.pack(pady=(10, 5))
        
        # Models listbox with scrollbar
        listbox_frame = ctk.CTkFrame(parent)
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.models_listbox = tk.Listbox(
            listbox_frame,
            font=("Arial", 11),
            selectmode=tk.SINGLE
        )
        self.models_listbox.pack(side="left", fill="both", expand=True)
        
        # Scrollbar for listbox
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.models_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.models_listbox.yview)
        
        # Model actions frame
        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Remove selected button
        self.remove_button = ctk.CTkButton(
            actions_frame,
            text="Remove Selected",
            command=self.remove_selected_model,
            width=self.REMOVE_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            state="disabled"
        )
        self.remove_button.pack(side="left", padx=5, pady=10)
        
        # Refresh models button
        self.refresh_button = ctk.CTkButton(
            actions_frame,
            text="Refresh",
            command=self.load_models,
            width=self.REFRESH_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.refresh_button.pack(side="left", padx=5, pady=10)
        
        # Download new model section
        download_frame = ctk.CTkFrame(parent)
        download_frame.pack(fill="x", pady=(0, 10))
        
        download_title = ctk.CTkLabel(
            download_frame,
            text="Download New Model:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        download_title.pack(pady=(10, 5))
        
        # Download input frame
        input_frame = ctk.CTkFrame(download_frame)
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Model name input
        self.model_name_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Enter model name (e.g., llama3.2:3b)",
            width=self.MODEL_INPUT_WIDTH,
            height=self.ENTRY_HEIGHT
        )
        self.model_name_entry.pack(side="left", padx=(10, 5), pady=10)
        
        # Download button
        self.download_button = ctk.CTkButton(
            input_frame,
            text="Download",
            command=self.download_model,
            width=self.DOWNLOAD_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT
        )
        self.download_button.pack(side="left", padx=5, pady=10)
        
        # Bind listbox selection event
        self.models_listbox.bind("<Button-1>", self.on_model_click)
        self.models_listbox.bind("<Key-Up>", self.on_model_key_select)
        self.models_listbox.bind("<Key-Down>", self.on_model_key_select)
        
        # Bind Enter key to download
        self.model_name_entry.bind("<Return>", lambda e: self.download_model())
    
    def setup_right_panel(self, parent):
        """Setup the right panel with model parameters."""
        # Parameters title
        params_title = ctk.CTkLabel(
            parent,
            text="Model Parameters:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        params_title.pack(pady=(10, 5))
        
        # Instructions
        instructions = ctk.CTkLabel(
            parent,
            text="Select a model to configure its parameters. Parameters are saved per model and used during AI processing.",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            wraplength=350
        )
        instructions.pack(pady=(0, 10))
        
        # Create scrollable frame for parameters
        self.params_scrollable = ctk.CTkScrollableFrame(parent)
        self.params_scrollable.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Initialize parameter widgets (will be populated when model is selected)
        self.param_widgets = {}
        
        # Save parameters button
        self.save_params_button = ctk.CTkButton(
            parent,
            text="Save Parameters",
            command=self.save_parameters,
            width=self.SAVE_BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            state="disabled"
        )
        self.save_params_button.pack(pady=(0, 10))
    
    def create_parameter_widgets(self, model_name):
        """Create parameter input widgets for a model based on its supported parameters."""
        # Clear existing widgets
        for widget in self.params_scrollable.winfo_children():
            widget.destroy()
        self.param_widgets = {}
        
        # Get model information including supported parameters
        model_info = self.ollama_handler.get_model_info(model_name)
        supported_params = model_info.get("supported_parameters", {})
        max_context_length = model_info.get("max_context_length")
        
        # Load current parameters for this model
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            config_manager = self.main_window.config_manager
            current_params = config_manager.get_model_parameters(model_name)
        else:
            current_params = {}
        
        # Show model info header
        info_frame = ctk.CTkFrame(self.params_scrollable)
        info_frame.pack(fill="x", pady=(0, 10))
        
        info_text = f"Model: {model_name}\n"
        if model_info.get("architecture"):
            info_text += f"Architecture: {model_info['architecture']}\n"
        if model_info.get("parameter_count"):
            info_text += f"Parameters: {model_info['parameter_count']}\n"
        if max_context_length:
            info_text += f"Max Context: {max_context_length:,}\n"
        if model_info.get("quantization"):
            info_text += f"Quantization: {model_info['quantization']}"
        
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=10, pady=5)
        
        # Only show parameters that are actually supported by this model
        if not supported_params:
            no_params_label = ctk.CTkLabel(
                self.params_scrollable,
                text="No configurable parameters found for this model.\nOnly basic parameters (temperature, top_p) will be used.",
                font=ctk.CTkFont(size=11),
                text_color="orange"
            )
            no_params_label.pack(pady=10)
            return
        
        # Create parameter widgets for each supported parameter
        for param_name, param_value in supported_params.items():
            if param_name == "temperature":
                # Ensure temperature is a float
                temp_value = current_params.get("temperature", param_value)
                try:
                    temp_value = float(temp_value)
                except (ValueError, TypeError):
                    temp_value = float(param_value)  # Use model default if conversion fails
                
                # Check if parameter was previously enabled
                enabled_params = current_params.get('_enabled_params', {})
                enabled = enabled_params.get('temperature', True)  # Default to enabled
                
                self.create_parameter_row(
                    "Temperature",
                    "temperature",
                    temp_value,
                    "Controls randomness (0.0 = deterministic, 1.0 = very random)",
                    min_val=0.0,
                    max_val=2.0,
                    step=0.1,
                    enabled=enabled
                )
            elif param_name == "top_p":
                # Ensure top_p is a float
                top_p_value = current_params.get("top_p", param_value)
                try:
                    top_p_value = float(top_p_value)
                except (ValueError, TypeError):
                    top_p_value = float(param_value)  # Use model default if conversion fails
                
                # Check if parameter was previously enabled
                enabled_params = current_params.get('_enabled_params', {})
                enabled = enabled_params.get('top_p', True)  # Default to enabled
                
                self.create_parameter_row(
                    "Top-p",
                    "top_p",
                    top_p_value,
                    "Nucleus sampling parameter (0.0-1.0)",
                    min_val=0.0,
                    max_val=1.0,
                    step=0.05,
                    enabled=enabled
                )
            elif param_name == "top_k":
                # Ensure top_k is an integer
                top_k_value = current_params.get("top_k", param_value)
                if isinstance(top_k_value, float):
                    top_k_value = int(top_k_value)
                else:
                    top_k_value = int(top_k_value)
                
                # Check if parameter was previously enabled
                enabled_params = current_params.get('_enabled_params', {})
                enabled = enabled_params.get('top_k', True)  # Default to enabled
                
                self.create_parameter_row(
                    "Top-k",
                    "top_k",
                    top_k_value,
                    "Limits number of tokens considered",
                    min_val=1,
                    max_val=100,
                    step=1,
                    enabled=enabled
                )
            elif param_name == "stop":
                # For stop parameter, we'll create a text input
                enabled_params = current_params.get('_enabled_params', {})
                enabled = enabled_params.get('stop', True)  # Default to enabled
                
                self.create_text_parameter_row(
                    "Stop Sequence",
                    "stop",
                    current_params.get("stop", param_value),
                    "Sequence that stops generation when encountered",
                    enabled=enabled
                )
            else:
                # Generic parameter for any other supported parameters
                enabled_params = current_params.get('_enabled_params', {})
                enabled = enabled_params.get(param_name, True)  # Default to enabled
                
                self.create_text_parameter_row(
                    param_name.title(),
                    param_name,
                    current_params.get(param_name, param_value),
                    f"Model-specific parameter: {param_name}",
                    enabled=enabled
                )
        
        # Add context length parameter if we have max context info
        if max_context_length:
            # Ensure num_ctx is an integer
            num_ctx_value = current_params.get("num_ctx", min(max_context_length, 4096))
            if isinstance(num_ctx_value, float):
                num_ctx_value = int(num_ctx_value)
            
            # Check if parameter was previously enabled
            enabled_params = current_params.get('_enabled_params', {})
            enabled = enabled_params.get('num_ctx', True)  # Default to enabled
            
            self.create_parameter_row(
                "Context Length",
                "num_ctx",
                num_ctx_value,
                f"Maximum context window size (up to {max_context_length:,})",
                min_val=512,
                max_val=max_context_length,
                step=256,
                enabled=enabled
            )
    
    def create_text_parameter_row(self, label, key, value, description, enabled=True):
        """Create a text parameter input row with checkbox."""
        # Main frame for parameter
        param_frame = ctk.CTkFrame(self.params_scrollable)
        param_frame.pack(fill="x", pady=2)
        
        # Enable/disable checkbox
        enable_checkbox = ctk.CTkCheckBox(
            param_frame,
            text="",
            width=self.CHECKBOX_WIDTH,
            command=lambda: self.toggle_parameter_enabled(key, enable_checkbox.get())
        )
        enable_checkbox.pack(side="left", padx=(5, 2), pady=5)
        enable_checkbox.select() if enabled else enable_checkbox.deselect()
        
        # Parameter label
        label_widget = ctk.CTkLabel(
            param_frame,
            text=label + ":",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.LABEL_WIDTH
        )
        label_widget.pack(side="left", padx=(5, 5), pady=5)
        
        # Text entry
        param_entry = ctk.CTkEntry(
            param_frame,
            width=self.ENTRY_WIDTH,
            font=ctk.CTkFont(size=10)
        )
        param_entry.insert(0, str(value))
        param_entry.pack(side="left", padx=5, pady=5)
        
        # Description
        desc_label = ctk.CTkLabel(
            param_frame,
            text=description,
            font=ctk.CTkFont(size=9),
            text_color="gray",
            wraplength=180
        )
        desc_label.pack(side="left", padx=(5, 5), pady=5)
        
        # Store widget reference
        self.param_widgets[key] = {
            'entry': param_entry,
            'checkbox': enable_checkbox,
            'type': 'text',
            'enabled': enabled
        }
        
        # Set initial enabled state
        self.update_parameter_enabled(key, enabled)
    
    def create_parameter_row(self, label, key, value, description, values=None, min_val=None, max_val=None, step=None, enabled=True):
        """Create a parameter input row with checkbox."""
        # Main frame for parameter
        param_frame = ctk.CTkFrame(self.params_scrollable)
        param_frame.pack(fill="x", pady=2)
        
        # Enable/disable checkbox
        enable_checkbox = ctk.CTkCheckBox(
            param_frame,
            text="",
            width=self.CHECKBOX_WIDTH,
            command=lambda: self.toggle_parameter_enabled(key, enable_checkbox.get())
        )
        enable_checkbox.pack(side="left", padx=(5, 2), pady=5)
        enable_checkbox.select() if enabled else enable_checkbox.deselect()
        
        # Parameter label
        label_widget = ctk.CTkLabel(
            param_frame,
            text=label + ":",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=self.LABEL_WIDTH
        )
        label_widget.pack(side="left", padx=(5, 5), pady=5)
        
        # Value input field
        value_entry = ctk.CTkEntry(
            param_frame,
            width=self.SLIDER_ENTRY_WIDTH,
            font=ctk.CTkFont(size=10)
        )
        
        # Set initial value with proper precision
        if isinstance(value, float):
            # Round to appropriate decimal places based on step
            if step and step >= 0.1:
                rounded_value = round(value, 1)
            elif step and step >= 0.01:
                rounded_value = round(value, 2)
            else:
                rounded_value = round(value, 3)
            value_entry.insert(0, str(rounded_value))
        else:
            value_entry.insert(0, str(value))
        
        value_entry.pack(side="left", padx=5, pady=5)
        
        # Parameter input widget
        if values:
            # Dropdown for predefined values
            widget = ctk.CTkOptionMenu(
                param_frame,
                values=values,
                width=self.LABEL_WIDTH,
                command=lambda val: self.update_parameter_entry(key, val, value_entry)
            )
            widget.set(str(value))
        else:
            # Slider for numeric values
            widget = ctk.CTkSlider(
                param_frame,
                from_=min_val,
                to=max_val,
                number_of_steps=int((max_val - min_val) / step) if step else 100,
                width=self.SLIDER_WIDTH,
                command=lambda v: self.update_parameter_entry(key, v, value_entry)
            )
            widget.set(value)
        
        widget.pack(side="left", padx=5, pady=5)
        
        # Bind Enter key to update slider from entry
        if not values:  # Only for sliders
            value_entry.bind('<Return>', lambda event: self.update_slider_from_entry(key, value_entry.get(), min_val, max_val))
        
        # Description
        desc_label = ctk.CTkLabel(
            param_frame,
            text=description,
            font=ctk.CTkFont(size=9),
            text_color="gray",
            wraplength=180
        )
        desc_label.pack(side="left", padx=(5, 5), pady=5)
        
        # Store widget references
        self.param_widgets[key] = {
            'widget': widget,
            'entry': value_entry,
            'checkbox': enable_checkbox,
            'type': 'option' if values else 'slider',
            'min_val': min_val,
            'max_val': max_val,
            'step': step,
            'enabled': enabled
        }
        
        # Set initial enabled state
        self.update_parameter_enabled(key, enabled)
    
    def update_parameter_display(self, key, value):
        """Update the parameter value display."""
        if key in self.param_widgets:
            self.param_widgets[key]['value_label'].configure(text=f"{value:.2f}")
    
    def update_parameter_entry(self, key, value, entry_widget):
        """Update the parameter entry field when slider/option changes."""
        if isinstance(value, float):
            # Round to appropriate decimal places to avoid floating point precision issues
            if key == 'temperature':
                rounded_value = round(value, 2)  # 2 decimal places for temperature
            elif key == 'top_p':
                rounded_value = round(value, 2)  # 2 decimal places for top_p
            elif key == 'repeat_penalty':
                rounded_value = round(value, 2)  # 2 decimal places for repeat_penalty
            else:
                rounded_value = round(value, 3)  # 3 decimal places for other floats
            
            # Clear and update entry
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, str(rounded_value))
        else:
            # Clear and update entry
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, str(value))
    
    def update_slider_from_entry(self, key, entry_value, min_val, max_val):
        """Update the slider when user enters a value in the entry field."""
        try:
            # Convert entry value to appropriate type
            widget_info = self.param_widgets.get(key, {})
            step = widget_info.get('step', 0.01)
            
            if key in ['num_ctx', 'num_predict', 'top_k']:
                # Integer parameters
                value = int(float(entry_value))
            elif key in ['temperature', 'top_p', 'repeat_penalty']:
                # Float parameters
                value = float(entry_value)
            else:
                # Generic parameter
                value = float(entry_value)
            
            # Clamp value to valid range
            if min_val is not None:
                value = max(min_val, value)
            if max_val is not None:
                value = min(max_val, value)
            
            # Update slider
            if key in self.param_widgets and self.param_widgets[key]['type'] == 'slider':
                self.param_widgets[key]['widget'].set(value)
                
        except (ValueError, TypeError) as e:
            print(f"Invalid value entered for {key}: {entry_value}")
            # Restore previous value
            if key in self.param_widgets:
                current_value = self.param_widgets[key]['widget'].get()
                self.param_widgets[key]['entry'].delete(0, 'end')
                self.param_widgets[key]['entry'].insert(0, str(current_value))
    
    def toggle_parameter_enabled(self, key, enabled):
        """Toggle parameter enabled/disabled state."""
        if key in self.param_widgets:
            self.param_widgets[key]['enabled'] = enabled
            self.update_parameter_enabled(key, enabled)
            # Ensure Save button stays enabled when toggling parameters
            if self.selected_model:
                print(f"DEBUG: Enabling Save button after toggling {key}")
                self.save_params_button.configure(state="normal")
    
    def update_parameter_enabled(self, key, enabled):
        """Update the enabled state of parameter widgets."""
        if key in self.param_widgets:
            widget_info = self.param_widgets[key]
            
            # Update visual state
            if enabled:
                widget_info['entry'].configure(state="normal")
                if 'widget' in widget_info:  # Only for slider/option parameters
                    widget_info['widget'].configure(state="normal")
                widget_info['checkbox'].configure(state="normal")
            else:
                widget_info['entry'].configure(state="disabled")
                if 'widget' in widget_info:  # Only for slider/option parameters
                    widget_info['widget'].configure(state="disabled")
                widget_info['checkbox'].configure(state="normal")  # Keep checkbox enabled
    
    def update_parameter_values_from_config(self, model_name):
        """Update parameter values from config without recreating widgets."""
        if not self.main_window or not hasattr(self.main_window, 'config_manager'):
            return
            
        config_manager = self.main_window.config_manager
        current_params = config_manager.get_model_parameters(model_name)
        enabled_params = current_params.get('_enabled_params', {})
        
        for key, widget_info in self.param_widgets.items():
            if key in current_params:
                # Update checkbox state
                enabled = enabled_params.get(key, True)
                widget_info['checkbox'].select() if enabled else widget_info['checkbox'].deselect()
                
                # Update entry field value
                value = current_params[key]
                widget_info['entry'].delete(0, 'end')
                widget_info['entry'].insert(0, str(value))
                
                # Update slider/option value if it exists
                if 'widget' in widget_info:
                    widget_info['widget'].set(value)
                
                # Update enabled state
                self.update_parameter_enabled(key, enabled)
    
    def load_models(self):
        """Load available models."""
        self.status_label.configure(text="Loading models...")
        self.refresh_button.configure(state="disabled")
        
        # Run in separate thread
        def load_thread():
            if self.ollama_handler.is_ollama_running():
                self.available_models = self.ollama_handler.get_available_models()
                self.dialog.after(0, self.update_models_list)
            else:
                self.dialog.after(0, self.show_ollama_error)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def update_models_list(self):
        """Update the models listbox."""
        self.models_listbox.delete(0, tk.END)
        
        if self.available_models:
            # Initialize default parameters for any new models
            self._initialize_new_model_parameters()
            
            for model in self.available_models:
                self.models_listbox.insert(tk.END, model)
            self.status_label.configure(text=f"Found {len(self.available_models)} models")
        else:
            self.models_listbox.insert(tk.END, "No models found")
            self.status_label.configure(text="No models found")
        
        self.refresh_button.configure(state="normal")
        self.update_remove_button_state()
    
    def _initialize_new_model_parameters(self):
        """Initialize default parameters for any new models that don't have them."""
        if not self.main_window or not hasattr(self.main_window, 'config_manager'):
            return
        
        config_manager = self.main_window.config_manager
        existing_params = config_manager.get_all_model_parameters()
        
        for model_name in self.available_models:
            if model_name not in existing_params:
                # Get model info to determine default parameters
                model_info = self.ollama_handler.get_model_info(model_name)
                supported_params = model_info.get("supported_parameters", {})
                max_context_length = model_info.get("max_context_length")
                
                # Create default parameters based on what the model supports
                default_params = {}
                
                # Add supported parameters with their default values
                for param_name, param_value in supported_params.items():
                    if param_name == "temperature":
                        default_params["temperature"] = 0.7
                    elif param_name == "top_p":
                        default_params["top_p"] = 0.9
                    elif param_name == "top_k":
                        default_params["top_k"] = int(param_value) if param_value.isdigit() else 40
                    elif param_name == "stop":
                        default_params["stop"] = str(param_value)
                    else:
                        # Generic parameter handling
                        default_params[param_name] = param_value
                
                # Add context length if we have max context info
                if max_context_length:
                    default_params["num_ctx"] = min(max_context_length, 4096)
                
                # Save the default parameters
                config_manager.save_model_parameters(model_name, default_params)
                print(f"Initialized default parameters for new model: {model_name}")
    
    def show_ollama_error(self):
        """Show error when Ollama is not running."""
        self.models_listbox.delete(0, tk.END)
        self.models_listbox.insert(tk.END, "Ollama service not running")
        self.status_label.configure(text="Ollama service not running")
        self.refresh_button.configure(state="normal")
        self.remove_button.configure(state="disabled")
        self.save_params_button.configure(state="disabled")
    
    def on_model_click(self, event):
        """Handle mouse click on model list."""
        # Let the click happen first, then check selection
        self.dialog.after(10, self.check_model_selection)
    
    def on_model_key_select(self, event):
        """Handle keyboard selection of model."""
        # Let the key event happen first, then check selection
        self.dialog.after(10, self.check_model_selection)
    
    def check_model_selection(self):
        """Check and handle model selection."""
        selection = self.models_listbox.curselection()
        
        if selection and self.available_models:
            new_selected_model = self.available_models[selection[0]]
            
            # Only create widgets if this is a different model
            if new_selected_model != self.selected_model:
                self.selected_model = new_selected_model
                try:
                    self.create_parameter_widgets(self.selected_model)
                except Exception as e:
                    print(f"Error creating parameter widgets: {e}")
                    print("DEBUG: Disabling Save button due to error")
                    self.save_params_button.configure(state="disabled")
                    return
            else:
                # Same model selected - just update values from config
                self.update_parameter_values_from_config(self.selected_model)
            
            print("DEBUG: Enabling Save button - model selected")
            self.save_params_button.configure(state="normal")
            self.status_label.configure(text=f"Selected model: {self.selected_model}")
        
        self.update_remove_button_state()
    
    def update_remove_button_state(self):
        """Update the remove button state based on selection."""
        selection = self.models_listbox.curselection()
        if selection and self.available_models:
            self.remove_button.configure(state="normal")
        else:
            self.remove_button.configure(state="disabled")
    
    def remove_selected_model(self):
        """Remove the selected model."""
        selection = self.models_listbox.curselection()
        if not selection:
            return
        
        model_name = self.available_models[selection[0]]
        
        # Confirm removal
        result = messagebox.askyesno(
            "Confirm Removal",
            f"Are you sure you want to remove the model '{model_name}'?\n\n"
            "This action cannot be undone and will free up disk space.",
            icon="warning"
        )
        
        if not result:
            return
        
        # Disable buttons during removal
        self.remove_button.configure(state="disabled", text="Removing...")
        self.refresh_button.configure(state="disabled")
        self.status_label.configure(text=f"Removing model '{model_name}'...")
        
        # Run removal in separate thread
        def remove_thread():
            success = self.ollama_handler.remove_model(model_name)
            self.dialog.after(0, lambda: self.removal_complete(success, model_name))
        
        threading.Thread(target=remove_thread, daemon=True).start()
    
    def removal_complete(self, success, model_name):
        """Handle model removal completion."""
        # Check if dialog still exists before configuring widgets
        try:
            self.remove_button.configure(text="Remove Selected")
            self.refresh_button.configure(state="normal")
        except tk.TclError:
            # Dialog was closed, ignore the error
            return
        
        if success:
            self.status_label.configure(text=f"Successfully removed model '{model_name}'")
            # Refresh the models list
            self.load_models()
            # Update main window if available
            if self.main_window and hasattr(self.main_window, 'edit_panel'):
                self.main_window.edit_panel.refresh_models()
        else:
            self.status_label.configure(text=f"Failed to remove model '{model_name}'")
            messagebox.showerror("Error", f"Failed to remove model '{model_name}'")
    
    def download_model(self):
        """Download a new model."""
        model_name = self.model_name_entry.get().strip()
        if not model_name:
            messagebox.showwarning("Warning", "Please enter a model name")
            return
        
        # Disable buttons during download
        self.download_button.configure(state="disabled", text="Downloading...")
        self.model_name_entry.configure(state="disabled")
        self.status_label.configure(text=f"Downloading model '{model_name}'...")
        
        # Run download in separate thread
        def download_thread():
            success = self.ollama_handler.pull_model(model_name)
            self.dialog.after(0, lambda: self.download_complete(success, model_name))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def download_complete(self, success, model_name):
        """Handle download completion."""
        # Check if dialog still exists before configuring widgets
        try:
            self.download_button.configure(text="Download", state="normal")
            self.model_name_entry.configure(state="normal")
            self.model_name_entry.delete(0, tk.END)
        except tk.TclError:
            # Dialog was closed, ignore the error
            return
        
        if success:
            self.status_label.configure(text=f"Successfully downloaded model '{model_name}'")
            # Refresh the models list
            self.load_models()
            # Update main window if available
            if self.main_window and hasattr(self.main_window, 'edit_panel'):
                self.main_window.edit_panel.refresh_models()
        else:
            self.status_label.configure(text=f"Failed to download model '{model_name}'")
            messagebox.showerror("Error", f"Failed to download model '{model_name}'")
    
    def save_parameters(self):
        """Save the current model parameters."""
        if not self.selected_model or not self.param_widgets:
            return
        
        # Collect current parameter values with proper type conversion
        parameters = {}
        enabled_params = {}
        
        for key, widget_info in self.param_widgets.items():
            try:
                # Get enabled state
                enabled = widget_info['checkbox'].get() == 1
                enabled_params[key] = enabled
                
                # Only process enabled parameters
                if not enabled:
                    continue
            except (KeyError, AttributeError) as e:
                print(f"Error processing parameter {key}: {e}")
                continue
                
            try:
                if widget_info['type'] == 'option':
                    value = widget_info['widget'].get()
                elif widget_info['type'] == 'text':
                    value = widget_info['entry'].get()
                else:
                    # For sliders, get value from entry field (more precise)
                    value = widget_info['entry'].get()
            except (KeyError, AttributeError) as e:
                print(f"Error getting value for parameter {key}: {e}")
                continue
            
            # Convert to appropriate type based on parameter name with proper precision
            if key in ['num_ctx', 'num_predict', 'top_k']:
                # Integer parameters
                try:
                    parameters[key] = int(float(value))  # Convert to int
                except (ValueError, TypeError):
                    parameters[key] = value  # Keep original if conversion fails
            elif key in ['temperature', 'top_p', 'repeat_penalty']:
                # Float parameters with proper precision rounding
                try:
                    float_val = float(value)
                    # Round to appropriate decimal places to avoid floating point precision issues
                    if key == 'temperature':
                        parameters[key] = round(float_val, 2)  # 2 decimal places for temperature
                    elif key == 'top_p':
                        parameters[key] = round(float_val, 2)  # 2 decimal places for top_p
                    elif key == 'repeat_penalty':
                        parameters[key] = round(float_val, 2)  # 2 decimal places for repeat_penalty
                    else:
                        parameters[key] = round(float_val, 3)  # 3 decimal places for other floats
                except (ValueError, TypeError):
                    parameters[key] = value  # Keep original if conversion fails
            else:
                # String parameters (quantization, stop, etc.)
                parameters[key] = str(value)
        
        # Include enabled state in parameters
        parameters['_enabled_params'] = enabled_params
        
        # Save to config
        if self.main_window and hasattr(self.main_window, 'config_manager'):
            config_manager = self.main_window.config_manager
            config_manager.save_model_parameters(self.selected_model, parameters)
            self.status_label.configure(text=f"Parameters saved for '{self.selected_model}'")
        else:
            messagebox.showerror("Error", "Cannot save parameters - config manager not available")