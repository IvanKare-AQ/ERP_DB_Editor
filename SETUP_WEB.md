# Web Application Setup Guide

This guide will help you set up and run the web-based ERP Database Editor.

## Prerequisites

- Python 3.8+ with virtual environment
- Node.js 18+ and npm

## Backend Setup (FastAPI)

1. **Activate your virtual environment:**
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API server:**
   ```bash
   # Option 1: Using the script (recommended)
   ./run_api.sh
   
   # Option 2: Direct command
   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
   ```

   The API will be available at: http://localhost:8001
   API documentation: http://localhost:8001/docs

## Frontend Setup (React)

1. **Navigate to web directory:**
   ```bash
   cd web
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:3000

## Testing the Setup

1. **Check API health:**
   ```bash
   curl http://localhost:8001/api/health
   ```

2. **View API documentation:**
   Open http://localhost:8001/docs in your browser

3. **Test frontend:**
   Open http://localhost:3000 in your browser

## Project Structure

```
ERP_DB_Editor/
├── src/
│   ├── api/              # FastAPI backend
│   │   ├── main.py       # Main FastAPI app
│   │   └── routes/       # API route handlers
│   │       ├── database.py    # Database operations
│   │       ├── items.py       # Item CRUD operations
│   │       ├── categories.py  # Category hierarchy
│   │       ├── ai.py          # AI-powered features
│   │       ├── config.py      # Configuration management
│   │       └── images.py      # Image handling
│   ├── backend/          # Shared backend logic
│   │   ├── json_handler.py    # JSON database operations
│   │   ├── image_handler.py   # Image processing & web search
│   │   ├── config_manager.py  # Configuration management
│   │   └── ...                # Other backend modules
│   └── gui/              # Desktop GUI (still available)
├── web/                  # React frontend
│   ├── src/
│   │   ├── App.jsx       # Main React component
│   │   ├── components/   # React components
│   │   │   ├── TreeView.jsx
│   │   │   ├── ManualEditor.jsx
│   │   │   ├── Toolbar.jsx
│   │   │   └── ...
│   │   └── main.jsx      # React entry point
│   ├── package.json
│   └── vite.config.js
├── data/                 # Database files
│   └── component_database.json
├── config/               # Configuration files
├── requirements.txt      # Python dependencies
└── run_api.sh           # Backend startup script
```

## Development Workflow

1. Start the backend API server (port 8001)
2. Start the frontend dev server (port 3000)
3. Make changes to either backend or frontend
4. Changes will hot-reload automatically

## Features

The web application includes:
- **Hierarchical Tree View**: Displays data in Category → Subcategory → Sub-subcategory hierarchy
- **Column Visibility**: Control which columns are displayed in the tree view
- **Manual Editor**: Edit item details including ERP Name, Type, Mfr. PN, Details, Manufacturer, Remarks
- **Image Management**: Add images via web search (DuckDuckGo) or local file upload
- **AI Features**: AI-powered category suggestions and field updates
- **Data Management**: Add, update, delete items with validation
- **Excel Export**: Export database to Excel format

## Troubleshooting

### Backend Issues
- **Port already in use**: If port 8001 is in use, change it in `run_api.sh` or the uvicorn command
- **Module not found**: Ensure virtual environment is activated and dependencies are installed
- **CORS errors**: Check that the frontend URL matches the CORS origins in `src/api/main.py`

### Frontend Issues
- **API connection errors**: Ensure the backend is running on port 8001
- **Build errors**: Run `npm install` again to ensure all dependencies are installed
- **Hot reload not working**: Check that both servers are running and ports are correct

## Production Deployment

1. **Build the React frontend:**
   ```bash
   cd web
   npm run build
   ```

2. **Run the FastAPI server:**
   The server will automatically serve the built React app from the `web/build` directory.

3. **Access the application:**
   - Development: http://localhost:3000 (frontend) → http://localhost:8001 (backend)
   - Production: http://localhost:8001 (serves both frontend and backend)

See `WEB_MIGRATION.md` for detailed migration information.
