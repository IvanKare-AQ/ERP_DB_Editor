# ERP Database Editor

A Python GUI application for editing ERP database files using CustomTkinter.

## Features

- **Excel File Operations**: Open, save, and save-as functionality for Excel files
- **Hierarchical Tree View**: Displays data in a tree format with Article Category → Article Subcategory → Article Sublevel → ERP Names hierarchy
- **Column Visibility Control**: Users can show/hide columns and save their view preferences
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
│   └── default_settings.json
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

### Automated Installation (Recommended)

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

### Manual Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Usage

1. **Open Excel File**: Click "Open Excel" to load an Excel file
2. **View Data**: Data is displayed in a hierarchical tree view
3. **Column Visibility**: Click "Column Visibility" to control which columns are shown
4. **Save View**: Click "Save View" to save your column visibility preferences
5. **Save Changes**: Use "Save" or "Save As" to save your changes

## Configuration

The application uses `config/default_settings.json` to store:
- Available columns
- Column visibility settings
- View preferences

## Requirements

- Python 3.8+
- customtkinter
- pandas
- openpyxl

## Development

The application follows a clean architecture pattern with:
- **GUI Layer**: CustomTkinter-based interface in `src/gui/`
- **Backend Layer**: Data handling and configuration in `src/backend/`
- **Main Application**: Entry point in `src/main.py`

## Future Enhancements

Requirements will be added to `App_Requirements.md` as the application develops.
