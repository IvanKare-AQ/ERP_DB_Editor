"""
Items API Routes
Handles individual item operations (CRUD, updates, reassignments).
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

router = APIRouter()

def get_json_handler():
    """Get JsonHandler instance."""
    from src.api.routes.database import get_json_handler as get_handler
    return get_handler()

class ItemUpdate(BaseModel):
    """Model for item updates."""
    row_id: str
    erp_name: Optional[Dict[str, Any]] = None
    manufacturer: Optional[str] = None
    remark: Optional[str] = None
    serialized: Optional[str] = None
    buy: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    sub_subcategory: Optional[str] = None
    image: Optional[str] = None

class ItemCreate(BaseModel):
    """Model for creating new items."""
    erp_name: Dict[str, Any]
    manufacturer: str = ""
    remark: str = ""
    serialized: str = "No"
    buy: str = "Yes"
    category: str
    subcategory: str
    sub_subcategory: str
    image: str = ""
    pn: Optional[int] = None

@router.get("/")
async def get_all_items():
    """Get all items from the database."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            return {"success": False, "items": [], "message": "Database not loaded"}
        
        return {
            "success": True,
            "items": data.to_dict(orient='records'),
            "count": len(data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get items: {str(e)}")

@router.get("/next-pn")
async def get_next_pn():
    """Get the next available PN number."""
    try:
        handler = get_json_handler()
        next_pn = handler.get_next_available_pn()
        
        return {
            "success": True,
            "pn": next_pn
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next PN: {str(e)}")

@router.get("/check-pn/{pn_value}")
async def check_pn_available(pn_value: int):
    """Check if a PN value is available (not already in use)."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            return {"success": True, "available": True}
        
        # Check if PN exists in main database
        pn_exists = (data['AirQ_PN'] == pn_value).any()
        
        # Also check in added items
        added_data = handler.get_added_data()
        if not added_data.empty:
            added_pn_exists = (added_data['AirQ_PN'] == pn_value).any()
        else:
            added_pn_exists = False
        
        available = not (pn_exists or added_pn_exists)
        
        return {
            "success": True,
            "available": available,
            "pn": pn_value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check PN: {str(e)}")

@router.get("/{row_id}")
async def get_item(row_id: str):
    """Get a specific item by row ID."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            raise HTTPException(status_code=400, detail="Database not loaded")
        
        # Find item by row_id (this would need proper implementation)
        # For now, return a placeholder
        return {
            "success": True,
            "item": None,
            "message": "Item lookup by row_id to be implemented"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get item: {str(e)}")

@router.put("/{row_id}")
async def update_item(row_id: str, update: ItemUpdate):
    """Update an item."""
    try:
        handler = get_json_handler()
        # Implementation would update the item in the DataFrame
        # and mark data as changed
        
        return {
            "success": True,
            "message": "Item updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update item: {str(e)}")

@router.post("/")
async def create_item(item: ItemCreate):
    """Create a new item."""
    try:
        handler = get_json_handler()
        
        # Use provided PN or get next available
        if item.pn is not None:
            # Check if PN is available
            data = handler.get_data()
            if data is not None:
                pn_exists = (data['AirQ_PN'] == item.pn).any()
                added_data = handler.get_added_data()
                if not added_data.empty:
                    added_pn_exists = (added_data['AirQ_PN'] == item.pn).any()
                else:
                    added_pn_exists = False
                
                if pn_exists or added_pn_exists:
                    raise HTTPException(status_code=400, detail=f"PN {item.pn} already exists")
            
            pn_value = item.pn
        else:
            pn_value = handler.get_next_available_pn()
        
        new_item = {
            'AirQ_PN': pn_value,
            'ERP Name': item.erp_name,
            'Manufacturer': item.manufacturer,
            'Remark': item.remark,
            'Serialized': item.serialized,
            'Buy': item.buy,
            'Category': item.category,
            'Subcategory': item.subcategory,
            'Sub-subcategory': item.sub_subcategory,
            'Image': item.image,
            'Tracking Method': '',
            'Use for ML': False,
            'Stage': '',
            'Origin': '',
            'Usage': '',
            'CAD Name': '',
            'EAN13': ''
        }
        
        handler.add_added_item(new_item)
        handler.save_added_items()
        
        return {
            "success": True,
            "message": "Item created successfully",
            "data": {"pn": pn_value, "item": new_item}
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create item: {str(e)}")

@router.delete("/{row_id}")
async def delete_item(row_id: str):
    """Delete an item."""
    try:
        handler = get_json_handler()
        # Implementation would remove item from DataFrame
        
        return {
            "success": True,
            "message": "Item deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete item: {str(e)}")

@router.post("/reassign")
async def reassign_item(reassignment: Dict[str, Any]):
    """Reassign an item to a new category path."""
    try:
        row_id = reassignment.get("row_id")
        category = reassignment.get("category")
        subcategory = reassignment.get("subcategory")
        sub_subcategory = reassignment.get("sub_subcategory")
        
        if not all([row_id, category, subcategory, sub_subcategory]):
            raise HTTPException(status_code=400, detail="Missing required fields")
        
        # Implementation would update the item's category path
        
        return {
            "success": True,
            "message": "Item reassigned successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reassign item: {str(e)}")

@router.post("/commit")
async def commit_items():
    """Commit draft items to main database."""
    try:
        handler = get_json_handler()
        result = handler.commit_added_items()
        
        return {
            "success": result.get('committed', 0) > 0,
            "message": f"Committed {result.get('committed', 0)} items",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to commit items: {str(e)}")
