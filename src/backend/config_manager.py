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