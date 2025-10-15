"""
Image Selection Dialog for ERP Database Editor
Modal dialog for selecting images via web search or local file.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
from typing import Optional, Callable


class ImageSelectionDialog:
    """Dialog for selecting and adding images to ERP items."""
    
    def __init__(self, parent, image_handler, initial_search: str = "", callback: Optional[Callable] = None):
        """Initialize the image selection dialog.
        
        Args:
            parent: Parent window
            image_handler: ImageHandler instance
            initial_search: Initial search phrase (usually PN)
            callback: Callback function to call with selected image path
        """
        self.image_handler = image_handler
        self.callback = callback
        self.selected_image = None
        self.selected_image_path = None
        self.search_results = []
        self.thumbnail_images = {}  # Store PhotoImage references
        
        # Create dialog window
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Add Image")
        self.dialog.geometry("900x700")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Setup the UI
        self.setup_ui(initial_search)
        
        # Center dialog on screen
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (700 // 2)
        self.dialog.geometry(f"900x700+{x}+{y}")
    
    def setup_ui(self, initial_search: str):
        """Setup the dialog UI components."""
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="Add Image to Item",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Search section
        search_frame = ctk.CTkFrame(self.dialog)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        search_label.pack(side="left", padx=(10, 5))
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Enter search phrase...",
            width=400
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.insert(0, initial_search)
        
        self.search_button = ctk.CTkButton(
            search_frame,
            text="Search Web",
            command=self.search_web_images,
            width=120
        )
        self.search_button.pack(side="left", padx=5)
        
        self.local_button = ctk.CTkButton(
            search_frame,
            text="Local File",
            command=self.select_local_file,
            width=120
        )
        self.local_button.pack(side="left", padx=5)
        
        # Results section
        results_label = ctk.CTkLabel(
            self.dialog,
            text="Search Results:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        results_label.pack(anchor="w", padx=20, pady=(10, 5))
        
        # Scrollable frame for results
        self.results_frame = ctk.CTkScrollableFrame(
            self.dialog,
            height=400
        )
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.dialog,
            text="Enter search phrase and click 'Search Web' or select 'Local File'",
            text_color="gray"
        )
        self.status_label.pack(pady=5)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(self.dialog)
        buttons_frame.pack(fill="x", padx=20, pady=20)
        
        self.select_button = ctk.CTkButton(
            buttons_frame,
            text="Add Selected Image",
            command=self.confirm_selection,
            width=150,
            height=40,
            state="disabled"
        )
        self.select_button.pack(side="left", padx=5)
        
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancel",
            command=self.dialog.destroy,
            width=100,
            height=40
        )
        cancel_button.pack(side="right", padx=5)
    
    def search_web_images(self):
        """Search for images on the web."""
        search_query = self.search_entry.get().strip()
        
        if not search_query:
            messagebox.showwarning("Warning", "Please enter a search phrase")
            return
        
        # Disable search button and show status
        self.search_button.configure(state="disabled", text="Searching...")
        self.status_label.configure(text="Searching for images...", text_color="blue")
        
        # Clear previous results
        self.clear_results()
        
        # Run search in thread to avoid blocking UI
        def search_thread():
            try:
                # Create a custom print function to capture retry messages
                import sys
                from io import StringIO
                
                # Capture print output
                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()
                
                try:
                    results = self.image_handler.web_search_images(search_query)
                    output = captured_output.getvalue()
                    
                    # Check if there were retry messages
                    if "Rate limited" in output or "Waiting" in output:
                        # Update status to show retry info
                        for line in output.split('\n'):
                            if line.strip():
                                self.dialog.after(0, lambda msg=line: self.status_label.configure(
                                    text=msg, text_color="orange"
                                ))
                    
                finally:
                    sys.stdout = old_stdout
                
                self.search_results = results
                
                # Update UI in main thread
                self.dialog.after(0, lambda: self.display_search_results(results))
                
            except Exception as e:
                self.dialog.after(0, lambda: self.search_error(str(e)))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def display_search_results(self, results):
        """Display search results with thumbnails."""
        self.search_button.configure(state="normal", text="Search Web")
        
        if not results:
            self.status_label.configure(
                text="No images found. Try a different search phrase.",
                text_color="orange"
            )
            return
        
        self.status_label.configure(
            text=f"Found {len(results)} images. Click on an image to select it.",
            text_color="green"
        )
        
        # Display results in grid
        for idx, result in enumerate(results):
            self.create_result_item(result, idx)
    
    def create_result_item(self, result, idx):
        """Create a result item with thumbnail."""
        # Create frame for this result
        item_frame = ctk.CTkFrame(self.results_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Download and display thumbnail in thread
        def load_thumbnail():
            try:
                # Try to use thumbnail URL first, fallback to main image
                url = result.get("thumbnail") or result.get("url")
                image = self.image_handler.download_image_from_url(url)
                
                if image:
                    # Resize for display
                    image.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Store reference to prevent garbage collection
                    self.thumbnail_images[idx] = photo
                    
                    # Update UI in main thread
                    self.dialog.after(0, lambda: self.display_thumbnail(item_frame, photo, result, idx))
            except Exception as e:
                print(f"Error loading thumbnail: {e}")
        
        # Placeholder while loading
        loading_label = ctk.CTkLabel(
            item_frame,
            text="Loading...",
            width=150,
            height=150
        )
        loading_label.pack(side="left", padx=10, pady=10)
        
        # Info label
        info_text = f"Image {idx + 1}\n{result.get('title', 'No title')[:50]}"
        if result.get('width') and result.get('height'):
            info_text += f"\n{result.get('width')}x{result.get('height')}"
        
        info_label = ctk.CTkLabel(
            item_frame,
            text=info_text,
            justify="left"
        )
        info_label.pack(side="left", padx=10, fill="x", expand=True)
        
        # Start loading thumbnail
        threading.Thread(target=load_thumbnail, daemon=True).start()
    
    def display_thumbnail(self, item_frame, photo, result, idx):
        """Display the loaded thumbnail."""
        # Remove loading label
        for widget in item_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") == "Loading...":
                widget.destroy()
                break
        
        # Create clickable thumbnail
        thumbnail_label = tk.Label(
            item_frame,
            image=photo,
            cursor="hand2"
        )
        thumbnail_label.image = photo  # Keep reference
        thumbnail_label.pack(side="left", padx=10, pady=10)
        thumbnail_label.bind("<Button-1>", lambda e: self.select_web_image(result, idx))
        
        # Highlight if selected
        if self.selected_image_path == result.get("url"):
            item_frame.configure(fg_color="#1f6aa5")
    
    def select_web_image(self, result, idx):
        """Handle selection of a web image."""
        self.selected_image_path = result.get("url")
        self.status_label.configure(
            text=f"Selected image {idx + 1}. Click 'Add Selected Image' to confirm.",
            text_color="green"
        )
        self.select_button.configure(state="normal")
        
        # Highlight selected item
        for widget in self.results_frame.winfo_children():
            widget.configure(fg_color=("gray90", "gray20"))
        
        # Highlight selected
        for i, widget in enumerate(self.results_frame.winfo_children()):
            if i == idx:
                widget.configure(fg_color="#1f6aa5")
    
    def select_local_file(self):
        """Select image from local file system."""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_image_path = file_path
            self.clear_results()
            
            # Display selected file info
            info_frame = ctk.CTkFrame(self.results_frame)
            info_frame.pack(fill="x", padx=5, pady=5)
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=f"Selected: {file_path}",
                font=ctk.CTkFont(size=12)
            )
            info_label.pack(padx=10, pady=10)
            
            self.status_label.configure(
                text="Local file selected. Click 'Add Selected Image' to confirm.",
                text_color="green"
            )
            self.select_button.configure(state="normal")
    
    def confirm_selection(self):
        """Process and save the selected image."""
        if not self.selected_image_path:
            messagebox.showwarning("Warning", "No image selected")
            return
        
        self.select_button.configure(state="disabled", text="Processing...")
        self.status_label.configure(text="Processing image...", text_color="blue")
        
        def process_thread():
            try:
                # Load image
                if self.selected_image_path.startswith("http"):
                    # Web image
                    image = self.image_handler.download_image_from_url(self.selected_image_path)
                else:
                    # Local file
                    image = Image.open(self.selected_image_path)
                
                if not image:
                    self.dialog.after(0, lambda: messagebox.showerror(
                        "Error", "Failed to load image"
                    ))
                    return
                
                # Generate filename from search query or use generic name
                search_query = self.search_entry.get().strip()
                if search_query:
                    filename = search_query.replace(" ", "_").replace("/", "_")
                else:
                    filename = "image"
                
                # Save image
                relative_path = self.image_handler.save_image(image, filename)
                
                if relative_path:
                    # Call callback with the relative path
                    self.dialog.after(0, lambda: self.success(relative_path))
                else:
                    self.dialog.after(0, lambda: messagebox.showerror(
                        "Error", "Failed to save image"
                    ))
                    
            except Exception as e:
                self.dialog.after(0, lambda: messagebox.showerror(
                    "Error", f"Failed to process image: {str(e)}"
                ))
            finally:
                self.dialog.after(0, lambda: self.select_button.configure(
                    state="normal", text="Add Selected Image"
                ))
        
        threading.Thread(target=process_thread, daemon=True).start()
    
    def success(self, relative_path):
        """Handle successful image addition."""
        if self.callback:
            self.callback(relative_path)
        messagebox.showinfo("Success", f"Image saved successfully:\n{relative_path}")
        self.dialog.destroy()
    
    def search_error(self, error_msg):
        """Handle search error."""
        self.search_button.configure(state="normal", text="Search Web")
        
        # Check if it's a rate limit error
        if "403" in error_msg or "Ratelimit" in error_msg or "rate" in error_msg.lower():
            self.status_label.configure(
                text="Rate limit exceeded. Please wait a few minutes or use 'Local File'.",
                text_color="red"
            )
            messagebox.showwarning(
                "Rate Limit Exceeded",
                "DuckDuckGo has rate-limited your searches.\n\n"
                "Solutions:\n"
                "1. Wait 2-5 minutes before searching again\n"
                "2. Use the 'Local File' button to select an image from your computer\n"
                "3. Try a different, more specific search phrase\n\n"
                "Rate limiting is temporary and will reset after a short wait."
            )
        else:
            self.status_label.configure(
                text=f"Search failed: {error_msg}",
                text_color="red"
            )
            messagebox.showerror("Search Error", f"Failed to search for images:\n{error_msg}")
    
    def clear_results(self):
        """Clear search results display."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        self.thumbnail_images.clear()
        self.search_results = []
        self.selected_image_path = None
        self.select_button.configure(state="disabled")

