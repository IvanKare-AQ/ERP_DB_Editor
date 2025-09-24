# ERP Database Editor - Requirements and Development Context
# This file contains the requirements and development context for the ERP Database Editor application

## Project Structure Requirements
- Application will have clean separation between GUI and backend elements
- GUI elements will be within src/gui folder
- Backend elements will be within src/backend folder
- src folder will contain main app and all application code
- data will contain all generated and used data and will be ignored for git
- GitHub repo for the project: git@github.com:IvanKare-AQ/ERP_DB_Editor.git

## UI/UX Requirements
- Modal windows will be used only when it really makes sense to reduce usage flow
- Clean and intuitive interface using CustomTkinter framework

## Initial Functional Requirements

### File Operations
- Open button to load Excel file
- Save button to save changes to the opened Excel sheet
- Save As to save in new file

### Data Display and Navigation
- Table will be represented in tree format with hierarchy:
  - "Article Category" as top level
  - "Article Subcategory" as second level
  - "Article Sublevel" as third level
  - All items from "ERP Names" column will be under relevant "Article Sublevel"
- This setting will be reflected in the existing default_settings.json file

### Column Management
- User will be able to set visible and non-visible columns
- "Save View" button that will store column visibility settings to default_settings.json

## Technical Requirements
- Python GUI application using CustomTkinter as GUI framework
- Excel file handling capabilities
- JSON configuration management
- Tree view implementation for hierarchical data display
- Column visibility management with persistence
- Use virtual environment (venv) for this application

## Future Requirements
- Requirements will be populated as application development progresses
- Additional features to be added based on development needs

## Documentation Requirements
- CHANGELOG.md will contain all changes throughout development step

## Column Visibility Requirements
- Column visibility functionality must properly hide/show columns in tree view
- Column visibility dialog must show all available columns regardless of current visibility state
- Column visibility settings must persist between application sessions
- Changes to column visibility must be immediately reflected in the tree view

## Dependencies
- customtkinter
- pandas (for Excel file handling)
- openpyxl (for Excel file reading/writing)
- tkinter (built-in, for additional GUI components)
