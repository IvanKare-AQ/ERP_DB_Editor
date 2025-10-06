"""
Ollama Handler for ERP Database Editor
Handles Ollama API integration for AI-powered editing functionality.
"""

import requests
import json
from typing import List, Dict, Any, Optional
import subprocess
import re
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
    
    def remove_model(self, model_name: str) -> bool:
        """Remove/delete a model from Ollama."""
        try:
            # Use subprocess to call ollama rm command
            result = subprocess.run(
                ["ollama", "rm", model_name],
                capture_output=True,
                text=True,
                timeout=60  # 1 minute timeout
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error removing model {model_name}: {e}")
            return False
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed information about a model including supported parameters."""
        try:
            result = subprocess.run(
                ["ollama", "show", model_name],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return self._parse_model_info(result.stdout)
            else:
                print(f"Error getting model info for {model_name}: {result.stderr}")
                return {}
                
        except Exception as e:
            print(f"Error getting model info for {model_name}: {e}")
            return {}
    
    def _parse_model_info(self, output: str) -> Dict[str, Any]:
        """Parse ollama show output to extract model information."""
        info = {
            "supported_parameters": {},
            "max_context_length": None,
            "quantization": None,
            "architecture": None,
            "parameter_count": None
        }
        
        lines = output.split('\n')
        in_parameters_section = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Extract architecture
            if line_stripped.startswith('architecture'):
                match = re.search(r'architecture\s+(\S+)', line_stripped)
                if match:
                    info["architecture"] = match.group(1)
            
            # Extract parameter count
            if line_stripped.startswith('parameters'):
                match = re.search(r'parameters\s+([0-9.]+[BKM]?)', line_stripped)
                if match:
                    info["parameter_count"] = match.group(1)
            
            # Extract context length
            if line_stripped.startswith('context length'):
                match = re.search(r'context length\s+(\d+)', line_stripped)
                if match:
                    info["max_context_length"] = int(match.group(1))
            
            # Extract quantization
            if line_stripped.startswith('quantization'):
                match = re.search(r'quantization\s+(\S+)', line_stripped)
                if match:
                    info["quantization"] = match.group(1)
            
            # Check if we're entering the Parameters section
            if line_stripped == 'Parameters':
                in_parameters_section = True
                continue
            
            # If we're in parameters section and hit a blank line or new section, stop
            if in_parameters_section and (line_stripped == '' or not line.startswith('  ')):
                in_parameters_section = False
                continue
            
            # Parse parameter lines (they start with spaces in the Parameters section)
            if in_parameters_section and line_stripped and line.startswith('  '):
                # Extract parameter name and value
                match = re.match(r'^([a-zA-Z_]+)\s+(.+)$', line_stripped)
                if match:
                    param_name = match.group(1)
                    param_value = match.group(2).strip()
                    info["supported_parameters"][param_name] = param_value
        
        return info
    
    def get_all_models_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information for all available models."""
        models_info = {}
        available_models = self.get_available_models()
        
        for model in available_models:
            models_info[model] = self.get_model_info(model)
        
        return models_info
    
    def _extract_erp_data_from_context(self, context: str) -> Dict[str, str]:
        """Extract ERP item data from context string."""
        erp_data = {
            'erp_name': 'Unknown',
            'category': 'Unknown', 
            'subcategory': 'Unknown',
            'sublevel': 'Unknown'
        }
        
        try:
            # Parse context string like: "Current ERP name: Screw M3x20, Category: Hardware, Subcategory: Fasteners, Sublevel: Screws"
            # or: "ERP: Screw M3x20, Cat: Hardware, Sub: Fasteners, Level: Screws"
            import re
            
            # Try different patterns
            patterns = [
                r"Current ERP name:\s*([^,]+)",
                r"ERP name:\s*([^,]+)", 
                r"ERP:\s*([^,]+)",
                r"Original name:\s*([^,]+)"
            ]
            
            for pattern in patterns:
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    erp_data['erp_name'] = match.group(1).strip()
                    break
            
            # Extract category
            category_patterns = [
                r"Category:\s*([^,]+)",
                r"Cat:\s*([^,]+)"
            ]
            for pattern in category_patterns:
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    erp_data['category'] = match.group(1).strip()
                    break
            
            # Extract subcategory
            subcategory_patterns = [
                r"Subcategory:\s*([^,]+)",
                r"Sub:\s*([^,]+)"
            ]
            for pattern in subcategory_patterns:
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    erp_data['subcategory'] = match.group(1).strip()
                    break
            
            # Extract sublevel
            sublevel_patterns = [
                r"Sublevel:\s*([^,]+)",
                r"Level:\s*([^,]+)"
            ]
            for pattern in sublevel_patterns:
                match = re.search(pattern, context, re.IGNORECASE)
                if match:
                    erp_data['sublevel'] = match.group(1).strip()
                    break
                    
        except Exception as e:
            print(f"Error parsing context: {e}")
            
        return erp_data

    def generate_erp_names(self, prompt: str, context: str, model_name: str, num_suggestions: int = 5, model_parameters: Dict[str, Any] = None) -> List[str]:
        """Generate ERP name suggestions using Ollama."""
        try:
            # Extract ERP data from context for template substitution
            erp_data = self._extract_erp_data_from_context(context)
            
            # Substitute template variables in the prompt
            substituted_prompt = prompt.format(
                erp_name=erp_data['erp_name'],
                category=erp_data['category'],
                subcategory=erp_data['subcategory'],
                sublevel=erp_data['sublevel']
            )
            
            # Prepare the full prompt with context
            full_prompt = f"""You are an expert at creating clear, descriptive ERP (Enterprise Resource Planning) names for products and components.

Context: {context}

Task: {substituted_prompt}

Please provide {num_suggestions} different ERP name suggestions. Each suggestion should be:
- Clear and descriptive
- Professional and technical
- Suitable for inventory management
- Unique and specific

Return only the ERP names, one per line, without numbering or bullet points."""

            # Use provided model parameters or defaults
            if model_parameters:
                # Get enabled parameters
                enabled_params = model_parameters.get("_enabled_params", {})
                
                options = {}
                
                # Temperature - only add if enabled (default enabled)
                if enabled_params.get("temperature", True):
                    options["temperature"] = float(model_parameters.get("temperature", 0.7))
                
                # Top-p - only add if enabled (default enabled)
                if enabled_params.get("top_p", True):
                    options["top_p"] = float(model_parameters.get("top_p", 0.9))
                
                # Only add additional parameters if they exist in the model_parameters AND are enabled
                if "top_k" in model_parameters and enabled_params.get("top_k", True):
                    options["top_k"] = int(model_parameters["top_k"])
                if "repeat_penalty" in model_parameters and enabled_params.get("repeat_penalty", True):
                    options["repeat_penalty"] = float(model_parameters["repeat_penalty"])
                if "num_ctx" in model_parameters and enabled_params.get("num_ctx", True):
                    options["num_ctx"] = int(model_parameters["num_ctx"])
                if "num_predict" in model_parameters and enabled_params.get("num_predict", True):
                    options["num_predict"] = int(model_parameters["num_predict"])
                if "stop" in model_parameters and enabled_params.get("stop", True):
                    options["stop"] = str(model_parameters["stop"])
            else:
                options = {
                    "temperature": 0.7,
                    "top_p": 0.9
                }

            payload = {
                "model": model_name,
                "prompt": full_prompt,
                "stream": False,
                "options": options
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=300  # Increased timeout to 5 minutes for larger models
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
