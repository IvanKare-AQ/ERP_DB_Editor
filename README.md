# ERP Database Editor

A Python application for editing ERP database files, available as both a desktop GUI (CustomTkinter) and a web application (FastAPI + React).

## Features

- **Dual Interface**: Desktop GUI (CustomTkinter) and Web Application (React + FastAPI)
- **Excel File Operations**: Open, save, and save-as functionality for Excel files
- **Hierarchical Tree View**: Displays data in a tree format with Article Category → Article Subcategory → Article Sublevel → ERP Names hierarchy
- **Column Visibility Control**: Users can show/hide columns and save their view preferences
- **Manual Editor**: Edit item details including ERP Name, Type, Mfr. PN, Details, Manufacturer, Remarks
- **Image Management**: Add images via web search (DuckDuckGo) or local file upload
- **AI Features**: AI-powered category suggestions and field updates
- **Clean Architecture**: Separation between GUI and backend components
- **Configuration Management**: Persistent settings stored in JSON format

## Project Structure

```
ERP_DB_Editor/
├── src/                    # Main application code
│   ├── main.py            # Application entry point
│   ├── gui/               # GUI components
│   │   ├── main_window.py # Main application window
│   │   ├── tree_view.py   # Tree view widget
│   │   └── column_visibility.py # Column visibility dialog
│   └── backend/           # Backend functionality
│       ├── excel_handler.py # Excel file operations
│       └── config_manager.py # Configuration management
├── config/                # Configuration files
│   └── application_setting.json
├── data/                  # Data files (ignored by git)
├── App_Requirements.md     # Project requirements and context
├── requirements.txt       # Python dependencies
├── install.sh            # Installation script for Linux/macOS
├── install.bat           # Installation script for Windows
├── test_installation.py  # Installation verification script
├── CHANGELOG.md          # Development changes log
└── README.md             # This file
```

## Installation

### Desktop Application

#### Automated Installation (Recommended)

**For Linux/macOS:**
```bash
./install.sh
```

**For Windows:**
```batch
install.bat
```

The installation scripts will automatically:
- Check Python installation
- Create virtual environment
- Install all required packages
- Create necessary directories
- Verify the installation

#### Manual Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the desktop application:
```bash
python src/main.py
```

### Web Application

For web application setup, see [SETUP_WEB.md](SETUP_WEB.md) for detailed instructions.

**Quick Start:**
1. Install Python dependencies (same as desktop):
   ```bash
   pip install -r requirements.txt
   ```

2. Install Node.js dependencies:
   ```bash
   cd web
   npm install
   ```

3. Start the backend API:
   ```bash
   ./run_api.sh
   ```

4. Start the frontend (in a new terminal):
   ```bash
   cd web
   npm run dev
   ```

5. Open http://localhost:3000 in your browser

## Usage

### Desktop Application
1. **Load Database**: The application automatically loads the database (`data/component_database.json`) on startup.
2. **View Data**: Data is displayed in a hierarchical tree view
3. **Column Visibility**: Click "Column Visibility" to control which columns are shown
4. **Save View**: Click "Save View" to save your column visibility preferences
5. **Save Changes**: Use "Save" to save your changes to the database

### Web Application
1. **Start Servers**: Ensure both backend (port 8001) and frontend (port 3000) are running
2. **Access Application**: Open http://localhost:3000 in your browser
3. **Edit Items**: Click on items in the tree view to edit them in the editor panel
4. **Add Items**: Click "New" to create a new item, then "Add Item" to save
5. **Manage Images**: Use "Add Image" to search the web or upload local images
6. **Column Visibility**: Use "Column Visibility" button to customize visible columns
7. **Save Changes**: Use "Save" to persist changes to the database

## Configuration

The application uses `config/application_setting.json` to store:
- Available columns
- Column visibility settings
- View preferences (filters, tree expansion state)
- AI model and prompt preferences

## Requirements

### Desktop Application
- Python 3.8+
- customtkinter
- pandas
- openpyxl

### Web Application
- Python 3.8+ (with FastAPI, uvicorn)
- Node.js 18+ and npm
- React 18+
- See `requirements.txt` and `web/package.json` for complete dependency lists

## Development

The application follows a clean architecture pattern with:
- **GUI Layer**: CustomTkinter-based interface in `src/gui/`
- **Backend Layer**: Data handling and configuration in `src/backend/`
- **Main Application**: Entry point in `src/main.py`

## Future Enhancements

Requirements will be added to `App_Requirements.md` as the application develops.
