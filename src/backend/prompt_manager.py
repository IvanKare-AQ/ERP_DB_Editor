"""
Prompt Manager for handling AI prompts storage and retrieval.
"""
import json
import os
from typing import Dict, List, Optional


class PromptManager:
    """Manages AI prompts storage and retrieval."""
    
    def __init__(self, config_dir: str = "config"):
        """Initialize the prompt manager.
        
        Args:
            config_dir: Directory where the prompts.json file is stored
        """
        self.config_dir = config_dir
        self.prompts_file = os.path.join(config_dir, "prompts.json")
        self._ensure_prompts_file()
    
    def _ensure_prompts_file(self):
        """Ensure the prompts.json file exists with default structure."""
        if not os.path.exists(self.prompts_file):
            os.makedirs(self.config_dir, exist_ok=True)
            default_prompts = {
                "prompts": {}
            }
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(default_prompts, f, indent=2, ensure_ascii=False)
    
    def save_prompt(self, name: str, description: str, prompt_text: str) -> bool:
        """Save a prompt to the prompts file.
        
        Args:
            name: Name/title of the prompt
            description: Brief description of the prompt
            prompt_text: The actual prompt text
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            # Load existing prompts
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Add new prompt
            data["prompts"][name] = {
                "description": description,
                "prompt": prompt_text
            }
            
            # Save back to file
            with open(self.prompts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving prompt: {e}")
            return False
    
    def get_prompts(self) -> Dict[str, Dict[str, str]]:
        """Get all saved prompts.
        
        Returns:
            Dictionary with prompt names as keys and prompt data as values
        """
        try:
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data.get("prompts", {})
        except Exception as e:
            print(f"Error loading prompts: {e}")
            return {}
    
    def get_prompt(self, name: str) -> Optional[str]:
        """Get a specific prompt by name.
        
        Args:
            name: Name of the prompt to retrieve
            
        Returns:
            The prompt text if found, None otherwise
        """
        prompts = self.get_prompts()
        return prompts.get(name, {}).get("prompt")
    
    def delete_prompt(self, name: str) -> bool:
        """Delete a prompt by name.
        
        Args:
            name: Name of the prompt to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # Load existing prompts
            with open(self.prompts_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Remove the prompt
            if name in data["prompts"]:
                del data["prompts"][name]
                
                # Save back to file
                with open(self.prompts_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                return True
            return False
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False
    
    def prompt_exists(self, name: str) -> bool:
        """Check if a prompt with the given name exists.
        
        Args:
            name: Name of the prompt to check
            
        Returns:
            True if prompt exists, False otherwise
        """
        prompts = self.get_prompts()
        return name in prompts
