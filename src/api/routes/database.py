"""
Database API Routes
Handles database loading, saving, and data operations.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, project_root)

from src.backend.json_handler import JsonHandler
from src.backend.config_manager import ConfigManager

router = APIRouter()

# Initialize handlers (singleton pattern)
_json_handler = None
_config_manager = None

def get_json_handler():
    """Get or create JsonHandler instance."""
    global _json_handler
    if _json_handler is None:
        _json_handler = JsonHandler()
    return _json_handler

def get_config_manager():
    """Get or create ConfigManager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

class DatabaseResponse(BaseModel):
    """Response model for database operations."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

@router.get("/load")
async def load_database():
    """Load the database from JSON file."""
    try:
        handler = get_json_handler()
        handler.load_file()
        handler.load_categories()
        handler.enrich_data()
        handler.load_added_items()
        
        data = handler.get_data()
        if data is None:
            raise HTTPException(status_code=500, detail="Failed to load data")
        
        return {
            "success": True,
            "message": "Database loaded successfully",
            "data": {
                "items": data.to_dict(orient='records'),
                "columns": list(data.columns),
                "row_count": len(data)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load database: {str(e)}")

@router.post("/save")
async def save_database(data: Dict[str, Any]):
    """Save the database to JSON file."""
    try:
        handler = get_json_handler()
        import pandas as pd
        
        # Convert data back to DataFrame
        items = data.get("items", [])
        if not items:
            raise HTTPException(status_code=400, detail="No items to save")
        
        df = pd.DataFrame(items)
        handler.save_file(data=df)
        
        return {
            "success": True,
            "message": "Database saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save database: {str(e)}")

@router.get("/info")
async def get_database_info():
    """Get database information."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            return {
                "success": False,
                "message": "Database not loaded",
                "data": None
            }
        
        return {
            "success": True,
            "message": "Database information",
            "data": {
                "row_count": len(data),
                "columns": list(data.columns),
                "file_path": handler.file_path
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get database info: {str(e)}")

@router.get("/columns")
async def get_columns():
    """Get all available columns."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        if data is None:
            return {
                "success": True,
                "data": []
            }
        columns = list(data.columns)
        return {
            "success": True,
            "data": columns
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get columns: {str(e)}")

@router.post("/export/excel")
async def export_to_excel(file_path: Optional[str] = None):
    """Export database to Excel file."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            raise HTTPException(status_code=400, detail="No data to export")
        
        # This would need to be implemented with file download
        # For now, return the data as JSON
        return {
            "success": True,
            "message": "Export functionality to be implemented",
            "data": data.to_dict(orient='records')
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export: {str(e)}")
