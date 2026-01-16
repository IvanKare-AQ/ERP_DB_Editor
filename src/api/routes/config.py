"""
Configuration API Routes
Handles application settings (column visibility, filters, view settings).
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, project_root)

from src.backend.config_manager import ConfigManager

router = APIRouter()

def get_config_manager():
    """Get ConfigManager instance."""
    from src.api.routes.database import get_config_manager as get_manager
    return get_manager()

@router.get("/column-visibility")
async def get_column_visibility():
    """Get column visibility settings."""
    try:
        manager = get_config_manager()
        visible_columns = manager.get_column_visibility()
        
        return {
            "success": True,
            "visible_columns": visible_columns or []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get column visibility: {str(e)}")

@router.post("/column-visibility")
async def save_column_visibility(columns: List[str]):
    """Save column visibility settings."""
    try:
        manager = get_config_manager()
        manager.save_column_visibility(columns)
        
        return {
            "success": True,
            "message": "Column visibility saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save column visibility: {str(e)}")

@router.get("/filters")
async def get_filters():
    """Get saved filter settings."""
    try:
        manager = get_config_manager()
        filters = manager.get_filters()
        
        return {
            "success": True,
            "filters": filters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get filters: {str(e)}")

@router.post("/filters")
async def save_filters(filters: Dict[str, Dict[str, Any]]):
    """Save filter settings."""
    try:
        manager = get_config_manager()
        manager.save_filters(filters)
        
        return {
            "success": True,
            "message": "Filters saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save filters: {str(e)}")

@router.get("/view-settings")
async def get_view_settings():
    """Get view settings (expansion state, etc.)."""
    try:
        manager = get_config_manager()
        settings = manager.get_view_settings()
        
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get view settings: {str(e)}")

@router.post("/view-settings")
async def save_view_settings(settings: Dict[str, Any]):
    """Save view settings."""
    try:
        manager = get_config_manager()
        manager.save_view_settings(settings)
        
        return {
            "success": True,
            "message": "View settings saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save view settings: {str(e)}")

@router.get("/ai-settings")
async def get_ai_settings():
    """Get AI settings."""
    try:
        manager = get_config_manager()
        settings = manager.get_ai_settings()
        
        return {
            "success": True,
            "settings": settings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get AI settings: {str(e)}")

@router.post("/ai-settings")
async def save_ai_settings(settings: Dict[str, Any]):
    """Save AI settings."""
    try:
        manager = get_config_manager()
        manager.save_ai_settings(settings)
        
        return {
            "success": True,
            "message": "AI settings saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save AI settings: {str(e)}")
