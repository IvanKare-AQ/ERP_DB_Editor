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
- "User ERP Name" column added after "Hierarchy" column for user modifications

### Data Editing and Modification
- Right panel edit section for modifying selected ERP items
- Input field that populates with priority: user modifications > existing "User ERP Name" > "ERP name"
- User can modify ERP names and save changes
- Category, subcategory, and sublevel dropdowns for item reassignment
- "Update Name" button to save user ERP name modifications
- "Reassign Item" button to move items to different categories
- All user modifications tracked in memory until saved
- Save functionality applies all modifications to Excel file
- Existing "User ERP Name" values from Excel files are preserved and displayed

## Technical Requirements
- Python GUI application using CustomTkinter as GUI framework
- Excel file handling capabilities
- JSON configuration management
- Tree view implementation for hierarchical data display
- Column visibility management with persistence
- Item selection and editing functionality
- User modification tracking and persistence
- Hierarchical dropdown population and filtering
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
- "Apply" button in column visibility dialog must only update view temporarily (not save to config)
- "Save View" button must be grayed out when there are no differences between current view and saved settings
- Proper separation between temporary view changes and persistent settings

## Data Filtering Requirements
- Excel-style filtering functionality for columns in tree view
- Filter types: contains, equals, starts with, ends with
- Filter dialog with individual column filter controls
- Multiple column filters can be applied simultaneously
- Filters must work with column visibility settings
- Clear individual filters and clear all filters functionality
- Real-time filter application with immediate tree view updates
- Filters must preserve hierarchical tree structure
- Filter settings must be saved and restored with Save View functionality
- Filters must be automatically loaded from settings file when application starts
- Filter state must be properly synchronized with Save View button state

## Data Export and Save Requirements
- "User ERP Name" column must be positioned immediately after "ERP name" column in saved Excel files
- Column reordering must preserve all existing data during save operations
- Save functionality must handle both scenarios: existing column in wrong position and missing column
- Consistent column order must be maintained across all save operations
- Duplicate columns must be cleaned up during save operations (keep only first occurrence)
- Existing "User ERP Name" values must be preserved when saving Excel files

## User Interface Requirements
- Status message bar at the bottom of the application window
- Status messages for all major operations (file operations, item selection, modifications, filters)
- File information display showing current loaded file name
- Status messages must be visible and provide clear feedback to users
- Status bar must be properly sized and positioned on application startup

## Data Integrity and Column Handling Requirements
- Excel data may contain duplicate column names with trailing spaces (e.g., "Article Sublevel " vs "Article Sublevel")
- Application must correctly identify and use the column containing actual data
- All tree view operations must use consistent column references throughout the application
- Row ID generation must use the correct column name to ensure proper item identification
- Dropdown population in edit panel must use the same column references as tree view operations
- User ERP Name updates must work correctly with the tree view's tag structure

## Visual Design Requirements
- Dark mode theme for table view with professional appearance
- Alternating row backgrounds for ERP items with subtle contrast
- Color-coded hierarchy levels that are visible in dark theme
- Consistent styling across all tree view elements
- Hover effects and selection highlighting that work with dark theme

## AI-Powered ERP Name Editing Requirements
- Integration with Ollama for AI-powered ERP name suggestions
- AI settings section with model selection dropdown
- Model refresh functionality to detect newly installed models
- Model download capability for pulling new models
- Prompt input field for custom AI instructions
- AI Results section for displaying generated names (increased height for 5 results)
- Preview functionality showing up to 5 AI-generated ERP name suggestions
- "Process Selected" button to apply AI prompt to all selected items individually
- "Process entire table" button to apply AI prompt to all items in the table
- Dynamic button state management: buttons convert to "Stop processing" during AI operations
- Stop processing functionality allowing users to cancel long-running AI operations
- Graceful termination of background AI processing with progress preservation
- AI model selection persistence in configuration file
- Automatic AI model refresh on application startup
- Threading for AI operations to prevent UI freezing
- Confirmation dialog before applying AI suggestions to prevent accidental changes
- Support for both single item and multiple item selection in AI operations
- Real-time progress tracking with stop instructions during processing
- Safe process termination ensuring no data loss or hanging threads

## Data Cleaning Requirements
- Multiline cell conversion functionality to convert multiline Excel cells to single line entries
- "NEN" prefix removal functionality to remove "NEN" and subsequent spaces from all cells
- Data cleaning buttons in toolbar for easy access to cleaning operations
- Confirmation dialogs for irreversible data cleaning operations
- Progress tracking and statistics for data cleaning operations
- Automatic tree view refresh after data cleaning operations
- Real-time status updates during data cleaning processes

## Data Integrity and Display Requirements
- Immediate visual updates after item reassignment operations
- Tree view must reflect user modifications in real-time without requiring file reload
- Proper handling of duplicate columns with trailing spaces in Excel data
- Clean Excel file output without duplicate columns during save operations
- Consistent column naming and structure throughout all operations
- User modifications must be applied to tree view data for immediate display

## Extended Field Editing Requirements
- Additional input fields for "Manufacturer" and "REMARK" columns
- Individual reset buttons for each input field (User ERP Name, Manufacturer, REMARK)
- Consolidated "Update All Fields" button to update all three fields simultaneously
- Priority system for field population: user modifications > original column values
- Real-time status updates for all field modifications
- Proper integration with save functionality to persist all field changes
- Individual field validation and error handling
- Consistent UI layout with inline reset buttons for each field

## User ERP Name Application Requirements
- "Apply User ERP Names" button to permanently move User ERP Name values to ERP name column
- Destructive operation that replaces existing ERP name values with User ERP Name values
- Clears User ERP Name column after successful application
- Confirmation dialog with clear warning about permanent nature of operation
- Real-time count of User ERP Names available for application
- Immediate tree view update to reflect changes
- Proper error handling and status feedback
- Integration with existing save functionality

## AI Prompt Management Requirements
- "Save Prompt" and "Select Prompt" buttons in AI Settings section
- Dynamic button state management based on prompt content
- Save Prompt button disabled when prompt field is empty
- Save Prompt button enabled when prompt field contains text
- Prompt selection dialog with two-panel layout (list + preview)
- Left panel showing prompt names and descriptions
- Right panel showing full prompt text preview
- Prompt deletion functionality with confirmation
- JSON-based prompt storage in config/prompts.json file
- Git integration for prompt file version control
- Prompt overwrite protection with user confirmation
- Real-time status updates for prompt operations
- Enhanced prompt selection dialog with additional management features
- Load to Editor functionality within selection dialog for modified prompts
- Edit Prompt functionality with full prompt text editing capability
- Duplicate functionality to create copies of prompts with " - Copy" suffix
- Delete Prompt functionality with confirmation dialogs
- Increased dialog height to accommodate all management buttons
- Prompt modification capabilities without leaving selection dialog
- Clear separation between prompt loading (Select AI Prompt dialog) and prompt saving (main application)
- Visual highlighting of selected prompts with subtle gray colors for better user experience
- Streamlined interface with Load to Editor as primary selection method
- Compact button layout with optimized sizing for better space utilization
- Smart duplicate naming system with conflict resolution (" - Copy", " - Copy (1)", etc.)
- Enhanced button state management for all prompt operations
- Read-only prompt preview in selection dialog for safe viewing
- Full text editing capability in Edit Prompt window
- Streamlined button interface with clear functionality separation
- Complete AI context generation with all ERP item fields (ERP name, category, subcategory, sublevel)
- Robust AI processing for both selected items and entire table operations

### Recent Enhancements (v1.0.0)
- **AI Prompt Management System**: Complete prompt save/load/edit/duplicate functionality
- **Enhanced User Interface**: Subtle highlighting, compact buttons, improved layouts
- **Smart Duplication**: Intelligent naming system for prompt copies
- **Professional Styling**: Consistent color scheme and button sizing
- **Improved Workflow**: Streamlined prompt management operations
- **Interface Refinements**: Read-only preview, editable edit window, streamlined buttons
- **AI Context Processing**: Complete ERP item context generation for accurate AI suggestions
- **Robust AI Operations**: Fixed context parsing for both selected items and entire table processing

### Latest Enhancements (v1.1.0)
- **Item Deletion Functionality**: Added "Delete Selected Item" button with confirmation dialog
- **Input Field Labels**: Added descriptive labels for User ERP Name, Manufacturer, and REMARK fields
- **Streamlined AI Interface**: Moved "Prompt Tool" button to AI Settings section for better organization
- **Removed Prompt Section**: Eliminated redundant prompt text area for cleaner interface
- **Enhanced Prompt Management**: "Load to Editor" functionality now works with stored prompts
- **Visual Prompt Status**: Added status label showing currently loaded prompt name
- **Improved User Experience**: Better organization and visual feedback throughout the interface

## Dependencies
- customtkinter
- pandas (for Excel file handling)
- openpyxl (for Excel file reading/writing)
- tkinter (built-in, for additional GUI components)
- requests (for Ollama API communication)
