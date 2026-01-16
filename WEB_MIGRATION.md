# Web Migration Guide

This document outlines the migration from CustomTkinter desktop application to FastAPI + React web application.

## Architecture Overview

### Backend (FastAPI)
- **Location**: `src/api/`
- **Main Entry**: `src/api/main.py`
- **Routes**: `src/api/routes/`
  - `database.py` - Database operations
  - `items.py` - Item CRUD operations
  - `categories.py` - Category hierarchy
  - `ai.py` - AI-powered features
  - `config.py` - Configuration management
  - `images.py` - Image handling

### Frontend (React)
- **Location**: `web/`
- **Framework**: React 18 + Vite
- **State Management**: React Query (TanStack Query)
- **UI Components**: To be implemented

## Current Status

### ✅ Completed
- FastAPI backend structure
- Basic API endpoints for all main operations
- React frontend setup with Vite
- CORS configuration
- Development server setup

### 🚧 In Progress
- Frontend components implementation
- Tree view component
- Real-time updates
- File upload handling

### 📋 TODO
- Implement React components for:
  - Tree view with hierarchical data
  - Item editor panel
  - AI editor interface
  - Column visibility dialog
  - Filter dialog
  - Image upload/search
- Add WebSocket support for real-time updates
- Implement authentication (if needed)
- Add error handling and loading states
- Optimize for large datasets
- Add unit tests

## Running the Application

### Backend
```bash
# Activate virtual environment
source venv/bin/activate

# Install web dependencies
pip install -r requirements.txt

# Run API server
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
# Or use the script:
./run_api.sh
```

### Frontend
```bash
cd web
npm install
npm run dev
```

## API Endpoints

### Database
- `GET /api/database/load` - Load database
- `POST /api/database/save` - Save database
- `GET /api/database/info` - Get database info
- `GET /api/database/columns` - Get all columns

### Items
- `GET /api/items/` - Get all items
- `GET /api/items/{row_id}` - Get specific item
- `PUT /api/items/{row_id}` - Update item
- `POST /api/items/` - Create new item
- `DELETE /api/items/{row_id}` - Delete item
- `POST /api/items/reassign` - Reassign item category
- `POST /api/items/commit` - Commit draft items

### Categories
- `GET /api/categories/` - Get category hierarchy
- `GET /api/categories/unique` - Get unique categories from data
- `GET /api/categories/properties` - Get category properties
- `POST /api/categories/suggest` - Get AI category suggestion

### AI
- `GET /api/ai/models` - Get available AI models
- `POST /api/ai/generate` - Generate ERP names
- `GET /api/ai/prompts` - Get all prompts
- `POST /api/ai/prompts` - Save prompt

### Config
- `GET /api/config/column-visibility` - Get column visibility
- `POST /api/config/column-visibility` - Save column visibility
- `GET /api/config/filters` - Get filters
- `POST /api/config/filters` - Save filters
- `GET /api/config/view-settings` - Get view settings
- `POST /api/config/view-settings` - Save view settings

### Images
- `POST /api/images/upload` - Upload image
- `GET /api/images/search` - Search images
- `GET /api/images/{path}` - Get image file

## Migration Strategy

1. **Phase 1**: Backend API (✅ Complete)
   - All endpoints defined
   - Backend logic wrapped

2. **Phase 2**: Core UI Components
   - Tree view component
   - Item list/table
   - Basic editor

3. **Phase 3**: Advanced Features
   - AI integration
   - Image handling
   - Real-time updates

4. **Phase 4**: Polish & Optimization
   - Performance optimization
   - Error handling
   - Testing

## Notes

- The backend reuses all existing backend classes (`JsonHandler`, `ConfigManager`, etc.)
- No changes needed to backend business logic
- Frontend will need to implement all UI components from scratch
- Consider using AG-Grid or similar for the tree view
- WebSocket can be added later for real-time collaboration
