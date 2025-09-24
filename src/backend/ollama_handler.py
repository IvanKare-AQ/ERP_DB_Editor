"""
Ollama Handler for ERP Database Editor
Handles Ollama API integration for AI-powered editing functionality.
"""

import requests
import json
from typing import List, Dict, Any, Optional
import subprocess
import os


class OllamaHandler:
    """Handles Ollama API operations for AI editing."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """Initialize the Ollama handler."""
        self.base_url = base_url
        
    def is_ollama_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
            return []
        except Exception as e:
            print(f"Error fetching models: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        """Download/pull a model from Ollama."""
        try:
            # Use subprocess to call ollama pull command
            result = subprocess.run(
                ["ollama", "pull", model_name],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error pulling model {model_name}: {e}")
            return False
    
    def generate_erp_names(self, prompt: str, context: str, model_name: str, num_suggestions: int = 5) -> List[str]:
        """Generate ERP name suggestions using Ollama."""
        try:
            # Prepare the full prompt with context
            full_prompt = f"""You are an expert at creating clear, descriptive ERP (Enterprise Resource Planning) names for products and components.

Context: {context}

Task: {prompt}

Please provide {num_suggestions} different ERP name suggestions. Each suggestion should be:
- Clear and descriptive
- Professional and technical
- Suitable for inventory management
- Unique and specific

Return only the ERP names, one per line, without numbering or bullet points."""

            payload = {
                "model": model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Parse the response to extract ERP names
                suggestions = []
                for line in response_text.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('*'):
                        # Clean up the line (remove numbering, bullets, etc.)
                        clean_name = line
                        # Remove common prefixes
                        for prefix in ['1.', '2.', '3.', '4.', '5.', '-', '*', '•']:
                            if clean_name.startswith(prefix):
                                clean_name = clean_name[len(prefix):].strip()
                        if clean_name:
                            suggestions.append(clean_name)
                
                # Return up to the requested number of suggestions
                return suggestions[:num_suggestions]
            else:
                print(f"Error generating suggestions: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error generating ERP names: {e}")
            return []
    
    def test_model(self, model_name: str) -> bool:
        """Test if a model is working properly."""
        try:
            payload = {
                "model": model_name,
                "prompt": "Hello, respond with just 'OK'",
                "stream": False
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            return response.status_code == 200
        except:
            return False
