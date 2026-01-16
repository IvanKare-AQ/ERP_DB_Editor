"""
AI API Routes
Handles AI-powered operations (ERP name generation, model management).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, project_root)

from src.backend.ollama_handler import OllamaHandler
from src.backend.prompt_manager import PromptManager
from src.backend.config_manager import ConfigManager

router = APIRouter()

def get_config_manager():
    """Get ConfigManager instance."""
    from src.api.routes.database import get_config_manager as get_manager
    return get_manager()

class GenerateRequest(BaseModel):
    """Request model for AI generation."""
    prompt: str
    model: str = "llama3.2"
    context: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None

@router.get("/models")
async def get_models():
    """Get available AI models."""
    try:
        handler = OllamaHandler()
        models = handler.get_available_models()
        
        return {
            "success": True,
            "models": models
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get models: {str(e)}")

@router.post("/generate")
async def generate_erp_names(request: GenerateRequest):
    """Generate ERP names using AI."""
    try:
        handler = OllamaHandler()
        
        if not handler.is_ollama_running():
            raise HTTPException(status_code=503, detail="Ollama is not running")
        
        # Generate names using the handler
        # This would need to be implemented based on the actual ollama_handler methods
        
        return {
            "success": True,
            "message": "Generation functionality to be implemented",
            "results": []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate names: {str(e)}")

@router.get("/prompts")
async def get_prompts():
    """Get all saved prompts."""
    try:
        manager = PromptManager()
        prompts = manager.get_all_prompts()
        
        return {
            "success": True,
            "prompts": prompts
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get prompts: {str(e)}")

@router.post("/prompts")
async def save_prompt(prompt_data: Dict[str, Any]):
    """Save a new prompt."""
    try:
        manager = PromptManager()
        result = manager.save_prompt(
            name=prompt_data.get("name"),
            description=prompt_data.get("description", ""),
            prompt=prompt_data.get("prompt")
        )
        
        return {
            "success": True,
            "message": "Prompt saved successfully",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save prompt: {str(e)}")
