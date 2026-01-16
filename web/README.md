# ERP Database Editor - Web Frontend

React-based web frontend for the ERP Database Editor application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The frontend will run on http://localhost:3000 and proxy API requests to http://localhost:8001.

## Build

To build for production:
```bash
npm run build
```

The build output will be in the `build/` directory, which can be served by the FastAPI backend.

## Development

- The API backend should be running on port 8001
- The frontend runs on port 3000
- API requests are automatically proxied during development
