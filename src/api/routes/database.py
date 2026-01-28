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

@router.get("/load-added")
async def load_added_items():
    """Load added/draft items from new_items.json."""
    try:
        handler = get_json_handler()
        handler.load_added_items()
        added_data = handler.get_added_data()
        
        if added_data is None or added_data.empty:
            return {
                "success": True,
                "message": "No added items found",
                "data": {
                    "items": [],
                    "columns": [],
                    "row_count": 0
                }
            }
        
        return {
            "success": True,
            "message": "Added items loaded successfully",
            "data": {
                "items": added_data.to_dict(orient='records'),
                "columns": list(added_data.columns),
                "row_count": len(added_data)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load added items: {str(e)}")

@router.post("/export/json")
async def export_to_json():
    """Export database to JSON file."""
    try:
        from fastapi.responses import Response
        import json
        
        handler = get_json_handler()
        handler.load_file()  # Ensure data is loaded
        data = handler.get_data()
        
        if data is None or data.empty:
            raise HTTPException(status_code=400, detail="No data to export")
        
        # Convert DataFrame to JSON
        json_data = data.to_dict(orient='records')
        
        # Convert to JSON string with proper formatting
        json_string = json.dumps(json_data, indent=2, ensure_ascii=False)
        json_bytes = json_string.encode('utf-8')
        
        # Return as response with proper headers
        return Response(
            content=json_bytes,
            media_type="application/json",
            headers={
                "Content-Disposition": "attachment; filename=component_database.json",
                "Content-Type": "application/json; charset=utf-8"
            }
        )
    except Exception as e:
        import traceback
        error_detail = f"Failed to export JSON: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@router.post("/export/excel")
async def export_to_excel():
    """Export database to Excel file. Separate endpoint for Excel export functionality."""
    try:
        from fastapi.responses import Response
        import io
        import pandas as pd
        
        handler = get_json_handler()
        handler.load_file()  # Ensure data is loaded
        data = handler.get_data()
        
        if data is None or data.empty:
            raise HTTPException(status_code=400, detail="No data to export")
        
        # Create a copy for export
        export_data = data.copy()
        
        # Convert ERP Name objects to full_name strings for Excel
        if 'ERP Name' in export_data.columns:
            def get_erp_full_name(erp_obj):
                if isinstance(erp_obj, dict):
                    return erp_obj.get('full_name', '')
                elif pd.isna(erp_obj):
                    return ''
                else:
                    return str(erp_obj)
            
            export_data['ERP Name'] = export_data['ERP Name'].apply(get_erp_full_name)
        
        # Create Excel file in memory
        output = io.BytesIO()
        try:
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                export_data.to_excel(writer, index=False, sheet_name='Components')
            
            # Get the bytes from the BytesIO object
            output.seek(0)
            excel_bytes = output.getvalue()
            
            # Return as response with proper headers
            return Response(
                content=excel_bytes,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={
                    "Content-Disposition": "attachment; filename=component_database.xlsx",
                    "Content-Type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                }
            )
        finally:
            output.close()
    except Exception as e:
        import traceback
        error_detail = f"Failed to export Excel: {str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)
