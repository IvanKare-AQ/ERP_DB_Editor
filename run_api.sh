#!/bin/bash
# Run FastAPI backend server

cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || echo "Virtual environment not found. Please activate it manually."

python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
