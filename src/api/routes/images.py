"""
Images API Routes
Handles image operations (upload, search, management).
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from typing import Optional
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, project_root)

from src.backend.image_handler import ImageHandler

router = APIRouter()

def get_image_handler():
    """Get ImageHandler instance."""
    handler = ImageHandler()
    return handler

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image file."""
    try:
        # Get database file path to initialize image handler properly
        from src.api.routes.database import get_json_handler
        handler = get_json_handler()
        db_path = handler.file_path
        
        # Initialize image handler with database path
        image_handler = ImageHandler(db_path)
        
        # Read file content
        contents = await file.read()
        
        # Generate filename
        import uuid
        file_ext = os.path.splitext(file.filename)[1] if file.filename else '.png'
        filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Save file to Images folder
        images_folder = image_handler.get_images_folder()
        file_path = os.path.join(images_folder, filename)
        
        with open(file_path, 'wb') as f:
            f.write(contents)
        
        # Return relative path
        relative_path = os.path.join(image_handler.settings["images_folder_name"], filename)
        
        return {
            "success": True,
            "file_path": relative_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

@router.post("/download")
async def download_image(request: dict):
    """Download an image from URL and save it."""
    try:
        from urllib.parse import urlparse
        import requests
        from PIL import Image as PILImage
        from io import BytesIO
        import uuid
        
        image_url = request.get("url")
        search_query = request.get("search_query", "")
        
        if not image_url:
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Get database file path to initialize image handler properly
        from src.api.routes.database import get_json_handler
        handler = get_json_handler()
        db_path = handler.file_path
        
        # Initialize image handler with database path
        image_handler = ImageHandler(db_path)
        
        # Download image
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        
        # Load and process image
        image = PILImage.open(BytesIO(response.content))
        
        # Resize if needed (based on settings)
        settings = image_handler.settings
        if settings.get("image_size"):
            size = settings["image_size"]
            if size.get("maintain_aspect_ratio", True):
                image.thumbnail((size["width"], size["height"]), PILImage.Resampling.LANCZOS)
            else:
                image = image.resize((size["width"], size["height"]), PILImage.Resampling.LANCZOS)
        
        # Generate filename
        file_ext = os.path.splitext(urlparse(image_url).path)[1] or '.png'
        if not file_ext or file_ext == '.':
            file_ext = '.png'
        filename = f"{uuid.uuid4().hex}{file_ext}"
        
        # Save to Images folder
        images_folder = image_handler.get_images_folder()
        file_path = os.path.join(images_folder, filename)
        
        # Save with appropriate format
        format = settings.get("image_format", "PNG")
        if format == "JPEG" and image.mode in ("RGBA", "LA", "P"):
            # Convert RGBA to RGB for JPEG
            rgb_image = PILImage.new("RGB", image.size, (255, 255, 255))
            if image.mode == "P":
                image = image.convert("RGBA")
            rgb_image.paste(image, mask=image.split()[-1] if image.mode == "RGBA" else None)
            image = rgb_image
        
        image.save(file_path, format=format, quality=settings.get("image_quality", 85))
        
        # Return relative path
        relative_path = os.path.join(image_handler.settings["images_folder_name"], filename)
        
        return {
            "success": True,
            "file_path": relative_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download image: {str(e)}")

@router.get("/search")
async def search_images(query: str, max_results: int = 10):
    """Search for images on the web."""
    try:
        # Get database file path to initialize image handler properly
        from src.api.routes.database import get_json_handler
        handler = get_json_handler()
        db_path = handler.file_path
        
        # Initialize image handler with database path
        image_handler = ImageHandler(db_path)
        
        # Perform web search
        results = image_handler.web_search_images(query, max_retries=3)
        
        # Limit results
        if len(results) > max_results:
            results = results[:max_results]
        
        # Format results for frontend
        formatted_results = []
        for result in results:
            formatted_results.append({
                "url": result.get("url", ""),
                "thumbnail": result.get("thumbnail", result.get("url", "")),
                "title": result.get("title", ""),
                "source": result.get("source", "")
            })
        
        return {
            "success": True,
            "results": formatted_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search images: {str(e)}")

@router.get("/{image_path:path}")
async def get_image(image_path: str):
    """Serve an image file."""
    try:
        from urllib.parse import unquote
        # Decode the image path
        decoded_path = unquote(image_path)
        
        # Get database file path to initialize image handler properly
        from src.api.routes.database import get_json_handler
        handler = get_json_handler()
        db_path = handler.file_path
        
        # Initialize image handler with database path
        image_handler = ImageHandler(db_path)
        
        # Load image - this returns a PIL Image object
        image = image_handler.load_image(decoded_path)
        
        if image:
            # Convert PIL Image to bytes
            from io import BytesIO
            from fastapi.responses import Response
            from PIL import Image as PILImage
            
            # Save to bytes
            img_bytes = BytesIO()
            # Determine format from file extension or default to PNG
            format = 'PNG'
            if decoded_path.lower().endswith(('.jpg', '.jpeg')):
                format = 'JPEG'
            elif decoded_path.lower().endswith('.gif'):
                format = 'GIF'
            
            image.save(img_bytes, format=format)
            img_bytes.seek(0)
            
            # Return image response
            return Response(content=img_bytes.getvalue(), media_type=f"image/{format.lower()}")
        else:
            # Try to find the file directly
            full_path = image_handler.get_images_folder()
            if os.path.isabs(decoded_path):
                full_path = decoded_path
            else:
                full_path = os.path.join(full_path, decoded_path)
            
            if os.path.exists(full_path):
                return FileResponse(full_path)
            else:
                raise HTTPException(status_code=404, detail="Image not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get image: {str(e)}")
