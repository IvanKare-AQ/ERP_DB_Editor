"""
Categories API Routes
Handles category hierarchy and operations.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, project_root)

from src.backend.json_handler import JsonHandler
from src.backend.category_suggester import CategorySuggester

router = APIRouter()

def get_json_handler():
    """Get JsonHandler instance."""
    from src.api.routes.database import get_json_handler as get_handler
    return get_handler()

@router.get("/")
async def get_categories():
    """Get the category hierarchy."""
    try:
        handler = get_json_handler()
        handler.load_categories()
        categories = handler.get_categories()
        
        return {
            "success": True,
            "categories": categories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get categories: {str(e)}")

@router.get("/unique")
async def get_unique_categories():
    """Get unique category values from data."""
    try:
        handler = get_json_handler()
        data = handler.get_data()
        
        if data is None:
            return {
                "success": True,
                "categories": [],
                "subcategories": {},
                "sub_subcategories": {}
            }
        
        categories = sorted(data['Category'].dropna().unique().tolist())
        subcategories = {}
        sub_subcategories = {}
        
        for cat in categories:
            cat_data = data[data['Category'] == cat]
            subcats = sorted(cat_data['Subcategory'].dropna().unique().tolist())
            subcategories[cat] = subcats
            
            for subcat in subcats:
                subcat_data = cat_data[cat_data['Subcategory'] == subcat]
                subsubcats = sorted(subcat_data['Sub-subcategory'].dropna().unique().tolist())
                sub_subcategories[f"{cat}::{subcat}"] = subsubcats
        
        return {
            "success": True,
            "categories": categories,
            "subcategories": subcategories,
            "sub_subcategories": sub_subcategories
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get unique categories: {str(e)}")

@router.get("/properties")
async def get_category_properties(category: str, subcategory: str, sub_subcategory: str):
    """Get properties for a specific category path."""
    try:
        handler = get_json_handler()
        props = handler.get_category_properties(category, subcategory, sub_subcategory)
        
        return {
            "success": True,
            "properties": props
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category properties: {str(e)}")

@router.post("/suggest")
async def suggest_category(suggestion_request: Dict[str, Any]):
    """Get AI-powered category suggestion."""
    try:
        handler = get_json_handler()
        suggester = CategorySuggester(json_handler=handler)
        
        suggestion = suggester.suggest_category(
            current_category=suggestion_request.get("current_category"),
            type_value=suggestion_request.get("type_value"),
            part_number=suggestion_request.get("part_number"),
            details=suggestion_request.get("details"),
            model_name=suggestion_request.get("model_name", "llama3.2"),
            use_ai=suggestion_request.get("use_ai", True)
        )
        
        return {
            "success": True,
            "suggestion": suggestion
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get category suggestion: {str(e)}")
