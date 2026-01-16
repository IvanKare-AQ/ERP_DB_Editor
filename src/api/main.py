"""
FastAPI Main Application
Entry point for the web API server.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.api.routes import database, categories, items, ai, config, images

app = FastAPI(
    title="ERP Database Editor API",
    description="REST API for ERP Database Editor web application",
    version="1.5.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(database.router, prefix="/api/database", tags=["database"])
app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
app.include_router(items.router, prefix="/api/items", tags=["items"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(config.router, prefix="/api/config", tags=["config"])
app.include_router(images.router, prefix="/api/images", tags=["images"])

# Serve static files in production (React build)
static_path = os.path.join(project_root, "web", "build")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")
    
    @app.get("/")
    async def serve_react_app():
        """Serve React app for production."""
        index_path = os.path.join(static_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "React app not built. Run 'npm run build' in web/ directory."}

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.5.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
