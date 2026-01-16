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
   # Option 1: Using the script
   ./run_api.sh
   
   # Option 2: Direct command
   python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
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
│   ├── backend/          # Existing backend logic (reused)
│   └── gui/              # Desktop GUI (still available)
├── web/                  # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.js
└── requirements.txt      # Python dependencies (updated)
```

## Development Workflow

1. Start the backend API server (port 8001)
2. Start the frontend dev server (port 3000)
3. Make changes to either backend or frontend
4. Changes will hot-reload automatically

## Next Steps

- Implement React components for the UI
- Add WebSocket support for real-time updates
- Implement authentication if needed
- Add error handling and loading states
- Optimize for large datasets

See `WEB_MIGRATION.md` for detailed migration information.
