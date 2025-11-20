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
from urllib.parse import urlparse, quote, unquote


class ImageHandler:
    """Handles image operations for the ERP Database Editor."""
    
    def __init__(self, db_file_path: Optional[str] = None):
        """Initialize the Image handler.
        
        Args:
            db_file_path: Path to the database file to determine image storage location
        """
        self.db_file_path = db_file_path
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
        """Get the path to the Images folder based on database file location.
        
        Returns:
            Path to the Images folder
        """
        if self.db_file_path:
            db_dir = os.path.dirname(os.path.abspath(self.db_file_path))
            images_folder = os.path.join(db_dir, self.settings["images_folder_name"])
        else:
            # Default to data folder if no database file path provided
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
    
    def _normalize_url(self, url: str) -> List[str]:
        """Generate multiple normalized versions of a URL to try.
        
        Args:
            url: Original URL
            
        Returns:
            List of URL variations to try
        """
        url_variations = [url]  # Start with original URL
        
        try:
            parsed = urlparse(url)
            
            # Decode any existing encoding
            decoded_path = unquote(parsed.path)
            
            # Variation 1: Properly encode the path (spaces -> %20, + -> %2B, etc.)
            encoded_path = quote(decoded_path, safe='/')
            normalized_url = f"{parsed.scheme}://{parsed.netloc}{encoded_path}"
            if normalized_url != url:
                url_variations.append(normalized_url)
            
            # Variation 2: Try with %20 instead of + for spaces
            if '+' in parsed.path:
                space_path = parsed.path.replace('+', '%20')
                space_url = f"{parsed.scheme}://{parsed.netloc}{space_path}"
                if space_url not in url_variations:
                    url_variations.append(space_url)
            
            # Variation 3: Try lowercase extension
            if parsed.path.upper().endswith(('.JPG', '.PNG', '.JPEG', '.GIF', '.WEBP')):
                lower_path = parsed.path[:-4] + parsed.path[-4:].lower()
                lower_url = f"{parsed.scheme}://{parsed.netloc}{lower_path}"
                if lower_url not in url_variations:
                    url_variations.append(lower_url)
            
            # Variation 4: Try uppercase extension
            if parsed.path.lower().endswith(('.jpg', '.png', '.jpeg', '.gif', '.webp')):
                upper_path = parsed.path[:-4] + parsed.path[-4:].upper()
                upper_url = f"{parsed.scheme}://{parsed.netloc}{upper_path}"
                if upper_url not in url_variations:
                    url_variations.append(upper_url)
                    
        except Exception as e:
            print(f"Error normalizing URL: {e}")
        
        return url_variations

    def download_image_from_url(self, url: str) -> Optional[Image.Image]:
        """Download an image from a URL with multiple retry strategies.
        
        Args:
            url: URL of the image to download
            
        Returns:
            PIL Image object or None if download fails
        """
        timeout = self.settings["web_search"]["timeout"]
        
        # Add headers to mimic a real browser and avoid 403 Forbidden errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'image',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'cross-site',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # Try multiple URL variations
        url_variations = self._normalize_url(url)
        last_error = None
        
        for idx, url_to_try in enumerate(url_variations):
            try:
                if idx > 0:
                    print(f"Trying alternative URL format ({idx + 1}/{len(url_variations)}): {url_to_try}")
                
                response = requests.get(url_to_try, timeout=timeout, stream=True, headers=headers)
                response.raise_for_status()
                
                # Successfully downloaded
                image = Image.open(BytesIO(response.content))
                if idx > 0:
                    print(f"✓ Successfully downloaded using alternative URL format")
                return image
                
            except requests.exceptions.HTTPError as e:
                last_error = e
                if e.response.status_code == 403:
                    # Don't try other variations for 403 errors
                    print(f"403 Forbidden: Website blocked image download from {url_to_try}")
                    print("Tip: Some websites block direct image downloads. Try using 'Local File' instead.")
                    return None
                elif e.response.status_code == 404:
                    # Try next variation for 404 errors
                    if idx == len(url_variations) - 1:
                        # Last attempt failed
                        print(f"404 Not Found: Image does not exist at {url}")
                        print("Possible reasons:")
                        print("  - The image may have been moved or deleted from the server")
                        print("  - The URL may be incorrect or outdated")
                        print("  - The website may have changed its URL structure")
                        print("Tip: Try searching for the image again or use 'Local File' option.")
                    continue
                else:
                    print(f"HTTP Error {e.response.status_code}: {e}")
                    if idx == len(url_variations) - 1:
                        return None
                    continue
                    
            except requests.exceptions.Timeout:
                print(f"Timeout: Failed to download image within {timeout} seconds")
                print("Tip: Try increasing the timeout in settings or check your internet connection.")
                return None
            except requests.exceptions.ConnectionError:
                print(f"Connection Error: Unable to reach {urlparse(url_to_try).netloc}")
                print("Tip: Check your internet connection and try again.")
                return None
            except Exception as e:
                last_error = e
                if idx == len(url_variations) - 1:
                    print(f"Error downloading image from URL: {e}")
                continue
        
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
    
    def set_db_file_path(self, db_file_path: str):
        """Update the database file path and Images folder location.
        
        Args:
            db_file_path: New path to the database file
        """
        self.db_file_path = db_file_path
        self.images_folder = self.get_images_folder()
    
    def get_relative_path(self, absolute_path: str) -> str:
        """Convert absolute image path to relative path from database file.
        
        Args:
            absolute_path: Absolute path to image file
            
        Returns:
            Relative path suitable for storing in database
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

