"""
Image Handler for ERP Database Editor
Handles image operations including loading, web search, and standardization.
"""

import os
import json
import requests
import time
from typing import Optional, List, Dict, Tuple
from PIL import Image
from io import BytesIO
from pathlib import Path


class ImageHandler:
    """Handles image operations for the ERP Database Editor."""
    
    def __init__(self, excel_file_path: Optional[str] = None):
        """Initialize the Image handler.
        
        Args:
            excel_file_path: Path to the Excel file to determine image storage location
        """
        self.excel_file_path = excel_file_path
        self.settings = self.load_settings()
        self.images_folder = self.get_images_folder()
        
    def load_settings(self) -> Dict:
        """Load image settings from configuration file."""
        settings_file = os.path.join(
            os.path.dirname(__file__), "..", "..", "config", "images_settings.json"
        )
        
        # Default settings if file doesn't exist
        default_settings = {
            "images_folder_name": "Images",
            "image_format": "PNG",
            "image_size": {
                "width": 800,
                "height": 600,
                "maintain_aspect_ratio": True
            },
            "image_quality": 85,
            "web_search": {
                "max_results": 10,
                "preferred_size": "medium",  # small, medium, large
                "timeout": 10
            }
        }
        
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                # Merge with defaults to ensure all keys exist
                return {**default_settings, **settings}
        except FileNotFoundError:
            # Create settings file with defaults
            os.makedirs(os.path.dirname(settings_file), exist_ok=True)
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(default_settings, f, indent=2)
            return default_settings
        except Exception as e:
            print(f"Error loading image settings: {e}")
            return default_settings
    
    def get_images_folder(self) -> str:
        """Get the path to the Images folder based on Excel file location.
        
        Returns:
            Path to the Images folder
        """
        if self.excel_file_path:
            excel_dir = os.path.dirname(os.path.abspath(self.excel_file_path))
            images_folder = os.path.join(excel_dir, self.settings["images_folder_name"])
        else:
            # Default to data folder if no Excel file path provided
            images_folder = os.path.join(
                os.path.dirname(__file__), "..", "..", "data", self.settings["images_folder_name"]
            )
        
        # Create folder if it doesn't exist
        os.makedirs(images_folder, exist_ok=True)
        return images_folder
    
    def load_image(self, image_path: str) -> Optional[Image.Image]:
        """Load an image from a file path.
        
        Args:
            image_path: Path to the image file (absolute or relative to Images folder)
            
        Returns:
            PIL Image object or None if loading fails
        """
        try:
            # Check if path is absolute
            if os.path.isabs(image_path):
                full_path = image_path
            else:
                # Relative path - check if it starts with Images/ folder name
                if image_path.startswith(self.settings["images_folder_name"] + "/"):
                    # Path already includes Images/ prefix, join with parent directory
                    excel_dir = os.path.dirname(self.images_folder)
                    full_path = os.path.join(excel_dir, image_path)
                else:
                    # Path is just filename, join with Images folder
                    full_path = os.path.join(self.images_folder, image_path)
            
            if not os.path.exists(full_path):
                print(f"Image not found: {full_path}")
                return None
            
            image = Image.open(full_path)
            return image
            
        except Exception as e:
            print(f"Error loading image: {e}")
            return None
    
    def web_search_images(self, search_query: str, max_retries: int = 3) -> List[Dict[str, str]]:
        """Search for images on the web using DuckDuckGo image search.
        
        Args:
            search_query: Search term for finding images
            max_retries: Maximum number of retry attempts on rate limit (default: 3)
            
        Returns:
            List of dictionaries containing image URLs and metadata
        """
        results = []
        
        try:
            # Using DuckDuckGo for image search (no API key required)
            try:
                from ddgs import DDGS
            except ImportError:
                # Fallback to old package name
                from duckduckgo_search import DDGS
            
            max_results = self.settings["web_search"]["max_results"]
            
            # Retry logic for rate limiting
            for attempt in range(max_retries):
                try:
                    # Add delay between attempts to avoid rate limiting
                    if attempt > 0:
                        wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                        print(f"Rate limited. Waiting {wait_time} seconds before retry {attempt + 1}/{max_retries}...")
                        time.sleep(wait_time)
                    
                    with DDGS() as ddgs:
                        search_results = ddgs.images(
                            search_query,
                            max_results=max_results
                        )
                        
                        for idx, result in enumerate(search_results):
                            results.append({
                                "index": idx,
                                "url": result.get("image", ""),
                                "thumbnail": result.get("thumbnail", ""),
                                "title": result.get("title", ""),
                                "source": result.get("source", ""),
                                "width": result.get("width", 0),
                                "height": result.get("height", 0)
                            })
                        
                        # Success - break out of retry loop
                        break
                        
                except Exception as search_error:
                    error_msg = str(search_error)
                    # Check if it's a rate limit error
                    if "403" in error_msg or "Ratelimit" in error_msg or "rate" in error_msg.lower():
                        if attempt < max_retries - 1:
                            continue  # Try again
                        else:
                            print(f"Rate limit exceeded after {max_retries} attempts. Please try again later.")
                            print("Tip: Wait a few minutes before searching again, or use local file selection.")
                    else:
                        # Different error - don't retry
                        raise search_error
            
        except ImportError:
            print("duckduckgo_search not installed. Install with: pip install duckduckgo-search")
        except Exception as e:
            print(f"Error searching for images: {e}")
            print("Tip: If you're experiencing rate limiting, try using the 'Select Local File' option instead.")
        
        return results
    
    def download_image_from_url(self, url: str) -> Optional[Image.Image]:
        """Download an image from a URL.
        
        Args:
            url: URL of the image to download
            
        Returns:
            PIL Image object or None if download fails
        """
        try:
            timeout = self.settings["web_search"]["timeout"]
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            return image
            
        except Exception as e:
            print(f"Error downloading image from URL: {e}")
            return None
    
    def unify_image(self, image: Image.Image) -> Image.Image:
        """Standardize image size and format according to settings.
        
        Args:
            image: PIL Image object to standardize
            
        Returns:
            Standardized PIL Image object
        """
        try:
            # Get target dimensions
            target_width = self.settings["image_size"]["width"]
            target_height = self.settings["image_size"]["height"]
            maintain_aspect = self.settings["image_size"]["maintain_aspect_ratio"]
            
            # Convert to RGB if necessary (for saving as JPEG/PNG)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image
            if maintain_aspect:
                # Maintain aspect ratio, fit within target dimensions
                image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
            else:
                # Resize to exact dimensions
                image = image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            return image
            
        except Exception as e:
            print(f"Error unifying image: {e}")
            return image
    
    def save_image(self, image: Image.Image, filename: str) -> Optional[str]:
        """Save an image to the Images folder with standardization.
        
        Args:
            image: PIL Image object to save
            filename: Desired filename (without extension)
            
        Returns:
            Relative path to saved image or None if save fails
        """
        try:
            # Unify the image first
            unified_image = self.unify_image(image)
            
            # Get format and quality from settings
            image_format = self.settings["image_format"].upper()
            quality = self.settings["image_quality"]
            
            # Add extension based on format
            if not filename.lower().endswith(f'.{image_format.lower()}'):
                filename = f"{filename}.{image_format.lower()}"
            
            # Full path to save
            full_path = os.path.join(self.images_folder, filename)
            
            # Save the image
            if image_format == 'PNG':
                unified_image.save(full_path, format='PNG', optimize=True)
            elif image_format in ('JPEG', 'JPG'):
                unified_image.save(full_path, format='JPEG', quality=quality, optimize=True)
            else:
                unified_image.save(full_path, format=image_format)
            
            # Return relative path
            relative_path = os.path.join(self.settings["images_folder_name"], filename)
            return relative_path
            
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
    
    def get_image_info(self, image_path: str) -> Optional[Dict]:
        """Get information about an image.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Dictionary with image information or None
        """
        try:
            image = self.load_image(image_path)
            if image:
                return {
                    "width": image.width,
                    "height": image.height,
                    "format": image.format,
                    "mode": image.mode,
                    "size_bytes": os.path.getsize(
                        os.path.join(self.images_folder, image_path) 
                        if not os.path.isabs(image_path) 
                        else image_path
                    )
                }
        except Exception as e:
            print(f"Error getting image info: {e}")
        
        return None
    
    def set_excel_file_path(self, excel_file_path: str):
        """Update the Excel file path and Images folder location.
        
        Args:
            excel_file_path: New path to the Excel file
        """
        self.excel_file_path = excel_file_path
        self.images_folder = self.get_images_folder()
    
    def get_relative_path(self, absolute_path: str) -> str:
        """Convert absolute image path to relative path from Excel file.
        
        Args:
            absolute_path: Absolute path to image file
            
        Returns:
            Relative path suitable for storing in Excel
        """
        try:
            # Get relative path from Images folder
            if self.images_folder in absolute_path:
                return os.path.relpath(absolute_path, os.path.dirname(self.images_folder))
            else:
                # Just return the filename with Images/ prefix
                return os.path.join(
                    self.settings["images_folder_name"], 
                    os.path.basename(absolute_path)
                )
        except Exception as e:
            print(f"Error getting relative path: {e}")
            return absolute_path

