"""
Configuration Manager for ERP Database Editor
Handles configuration file operations including column visibility settings.
"""

import json
import os
from typing import List, Dict, Any, Optional


class ConfigManager:
    """Manages configuration settings for the ERP Database Editor."""
    
    def __init__(self, config_file: str = "config/default_settings.json"):
        """Initialize the configuration manager."""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default configuration
                return self.get_default_config()
        except Exception as e:
            print(f"Warning: Failed to load config file: {e}")
            return self.get_default_config()
            
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "rows": [
                "SN",
                "SKU NR", 
                "KEN NAME",
                "ERP name",
                "CAD name",
                "Electronics",
                "Article Category",
                "Article Subcategory",
                "Article Sublevel",
                "Product Value",
                "Manufacturer",
                "SKU",
                "EAN 13",
                "Unit",
                "Supplier",
                "Expiry Date (Y/N)",
                "Tracking Method",
                "Procurement Method (Buy/Make)",
                "REMARK"
            ],
            "column_visibility": {},
            "view_settings": {}
        }
        
    def save_config(self) -> None:
        """Save configuration to file."""
        try:
            # Ensure config directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise Exception(f"Failed to save config file: {str(e)}")
            
    def get_column_visibility(self) -> Optional[List[str]]:
        """Get column visibility settings."""
        return self.config.get("column_visibility", {}).get("visible_columns")
        
    def save_column_visibility(self, visible_columns: List[str]) -> None:
        """Save column visibility settings."""
        if "column_visibility" not in self.config:
            self.config["column_visibility"] = {}
            
        self.config["column_visibility"]["visible_columns"] = visible_columns
        self.save_config()
        
    def get_view_settings(self) -> Dict[str, Any]:
        """Get view settings."""
        return self.config.get("view_settings", {})
        
    def save_view_settings(self, settings: Dict[str, Any]) -> None:
        """Save view settings."""
        self.config["view_settings"] = settings
        self.save_config()
        
    def get_available_columns(self) -> List[str]:
        """Get available columns from configuration."""
        return self.config.get("rows", [])
        
    def update_available_columns(self, columns: List[str]) -> None:
        """Update available columns in configuration."""
        self.config["rows"] = columns
        self.save_config()
    
    def save_filters(self, filters: Dict[str, Dict[str, Any]]) -> None:
        """Save filter settings."""
        if "view_settings" not in self.config:
            self.config["view_settings"] = {}
        
        self.config["view_settings"]["filters"] = filters
        self.save_config()
    
    def get_filters(self) -> Dict[str, Dict[str, Any]]:
        """Get saved filter settings."""
        return self.config.get("view_settings", {}).get("filters", {})
    
    def get_ai_settings(self) -> Dict[str, Any]:
        """Get AI settings."""
        return self.config.get("ai_settings", {})
    
    def save_ai_settings(self, settings: Dict[str, Any]) -> None:
        """Save AI settings."""
        self.config["ai_settings"] = settings
        self.save_config()
    
    def get_selected_model(self) -> Optional[str]:
        """Get selected AI model."""
        return self.config.get("ai_settings", {}).get("selected_model")
    
    def save_selected_model(self, model_name: str) -> None:
        """Save selected AI model."""
        if "ai_settings" not in self.config:
            self.config["ai_settings"] = {}
        
        self.config["ai_settings"]["selected_model"] = model_name
        self.save_config()
    
    def get_selected_prompt(self) -> Optional[str]:
        """Get selected AI prompt key."""
        return self.config.get("ai_settings", {}).get("selected_prompt")
    
    def save_selected_prompt(self, prompt_key: str) -> None:
        """Save selected AI prompt key."""
        if "ai_settings" not in self.config:
            self.config["ai_settings"] = {}
        
        self.config["ai_settings"]["selected_prompt"] = prompt_key
        self.save_config()
    
    def get_selected_prompt_text(self) -> Optional[str]:
        """Get the actual prompt text for the selected prompt key."""
        prompt_key = self.get_selected_prompt()
        if not prompt_key:
            return None
        
        # Load prompts from prompts.json
        try:
            prompts_file = os.path.join(os.path.dirname(__file__), "..", "..", "config", "prompts.json")
            with open(prompts_file, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
            
            # Get the prompt text for the selected key
            prompt_info = prompts_data.get("prompts", {}).get(prompt_key)
            if prompt_info:
                return prompt_info.get("prompt")
            
        except Exception as e:
            print(f"Error loading prompt text for key '{prompt_key}': {e}")
        
        return None
    
    def get_available_prompts(self) -> Dict[str, Dict[str, str]]:
        """Get all available prompts from prompts.json."""
        try:
            prompts_file = os.path.join(os.path.dirname(__file__), "..", "..", "config", "prompts.json")
            with open(prompts_file, 'r', encoding='utf-8') as f:
                prompts_data = json.load(f)
            
            return prompts_data.get("prompts", {})
            
        except Exception as e:
            print(f"Error loading prompts: {e}")
            return {}
    
    def get_model_parameters(self, model_name: str) -> Dict[str, Any]:
        """Get parameters for a specific model."""
        if "model_parameters" not in self.config:
            self.config["model_parameters"] = {}
        
        # If model exists, return its parameters
        if model_name in self.config["model_parameters"]:
            return self.config["model_parameters"][model_name]
        
        # Model not found - create default parameters based on model type
        default_params = self._create_default_parameters_for_model(model_name)
        
        # Save the default parameters for future use
        self.config["model_parameters"][model_name] = default_params
        self.save_config()
        
        return default_params
    
    def _create_default_parameters_for_model(self, model_name: str) -> Dict[str, Any]:
        """Create default parameters for a model based on its name/type."""
        # Basic default parameters
        default_params = {
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        # Add model-specific defaults based on common patterns
        if "gpt" in model_name.lower():
            # GPT models typically support basic parameters
            default_params.update({
                "num_ctx": 4096,
                "num_predict": 512
            })
        elif "gemma" in model_name.lower():
            # Gemma models typically support more parameters
            default_params.update({
                "top_k": 40,
                "repeat_penalty": 1.1,
                "num_ctx": 4096,
                "num_predict": 512
            })
        elif "llama" in model_name.lower():
            # Llama models
            default_params.update({
                "top_k": 40,
                "repeat_penalty": 1.1,
                "num_ctx": 2048,
                "num_predict": 256
            })
        else:
            # Generic model defaults
            default_params.update({
                "num_ctx": 2048,
                "num_predict": 256
            })
        
        return default_params
    
    def save_model_parameters(self, model_name: str, parameters: Dict[str, Any]) -> None:
        """Save parameters for a specific model."""
        if "model_parameters" not in self.config:
            self.config["model_parameters"] = {}
        
        self.config["model_parameters"][model_name] = parameters
        self.save_config()
    
    def get_all_model_parameters(self) -> Dict[str, Dict[str, Any]]:
        """Get all model parameters."""
        return self.config.get("model_parameters", {})