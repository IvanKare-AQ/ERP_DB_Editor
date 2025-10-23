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
- Master column list (`all_columns`) maintained to ensure all columns always accessible
- `get_all_columns()` method provides access to complete column list
- Column visibility settings must persist between application sessions
- Changes to column visibility must be immediately reflected in the tree view
- "Apply" button in column visibility dialog must only update view temporarily (not save to config)
- "Save View" button must be grayed out when there are no differences between current view and saved settings
- Proper separation between temporary view changes and persistent settings
- Hidden columns must remain accessible for re-showing through visibility dialog

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

### Tabbed Interface Redesign (v1.2.0)
- **Modular Edit Panel Architecture**: Restructured right panel into three specialized tabs
  - **Manual Tab (✏️)**: Manual editing, reassignment, and data cleaning tools
  - **AI Tab (🤖)**: AI-powered editing with model management and prompt tools
  - **ML Tab (🧠)**: Placeholder for future machine learning features
- **Fixed Width Layout**: Right panel now uses consistent 1000px width across all tabs
- **Component Separation**: Each tab is a self-contained module with dedicated file
  - `manual_editor.py`: Manual editing functionality (User ERP Name, Manufacturer, REMARK)
  - `ai_editor.py`: AI tools and model management (completely self-contained)
  - `ml_editor.py`: ML placeholder for future expansion
- **Enhanced Data Cleaning**: Moved "Convert Multiline" and "Remove NEN" buttons to Manual tab
- **Unified UI Constants**: Width and height parameters standardized across all UI components
  - Consistent button heights (35px standard, 90px for reassign)
  - Standardized input field widths (400px)
  - Unified spacing and padding values
- **Self-Contained AI Editor**: AI functionality now handles its own initialization
  - Automatic model refresh on startup
  - Configuration loading integrated within AI editor
  - Independent status updates and error handling
- **Professional Tab Icons**: Unicode icons for quick visual identification of tab purposes
- **Bug Fixes**: Critical fixes for AI prompt selection and item reassignment
  - AI prompt selection now works correctly with Generate and Process buttons
  - Prompt changes take effect immediately without requiring "Save View"
  - Reassigned items now retain their new category information for further reassignment
  - Category/subcategory/sublevel dropdowns populate correctly after reassignment
- **User ERP Name Parsing System**: Advanced parsing and editing capabilities for structured naming
  - Automatic parsing of User ERP Name into Type, PN (Part Number), and Details components
  - Format: Type_PN_Details (separated by underscores)
  - Bidirectional synchronization between User ERP Name and parsed fields
  - Real-time updates when editing either User ERP Name or individual components
  - Underscore to hyphen conversion buttons for all three fields
  - NO-PN quick-insert button for items without part numbers
  - Flexible naming convention support (structural _ vs descriptive - separators)
  - Visual separator between standard fields and parsed fields for clarity
- **Image Management System**: Complete image handling with web search and preview
  - Automatic Image column creation in Excel files (positioned after ERP name)
  - Image preview display (150x150) in Manual Editing tab
  - Modal dialog for image selection with multiple sources
  - Web image search using DuckDuckGo (no API key required)
  - Local file selection via file browser with full preview (up to 400x400)
  - Local file preview displays metadata (filename, dimensions, format, size)
  - Robust image download with URL normalization and retry strategies
  - Automatic handling of URL encoding variations (spaces, +, special characters)
  - Support for case-insensitive file extensions (.jpg vs .JPG)
  - Intelligent retry logic for unreliable image URLs
  - Enhanced error messages with specific reasons and helpful tips
  - Automatic image processing and standardization
  - Image storage in Images/ folder alongside Excel file
  - Configurable image settings (size, format, quality)
  - Relative path storage in Excel for portability
  - Support for PNG, JPEG, WEBP, and other common formats
  - Thumbnail preview in search results
  - Multi-item selection handling with placeholder icons

## AI Model Management Requirements
- **AI Model Management System**: Complete model management functionality
  - Model Manager dialog for downloading, removing, and configuring AI models
  - Model parameter tuning with sliders, input fields, and checkboxes
  - Dynamic parameter display based on model capabilities (using `ollama show`)
  - Parameter enable/disable functionality with persistent settings
  - Model-specific parameter storage in configuration file
  - Real-time parameter validation and type conversion
  - Bidirectional synchronization between sliders and input fields
  - Save button state management for parameter changes
  - Model information display (architecture, parameters, context length, quantization)
  - Automatic parameter initialization for new models
  - Robust error handling for model operations

## AI Prompt Template System Requirements
- **Template Variable Substitution**: Automatic replacement of prompt template variables
  - Support for `{erp_name}`, `{category}`, `{subcategory}`, `{sublevel}` variables
  - Automatic extraction of ERP item data from context strings
  - Template substitution before sending prompts to AI models
  - Consistent behavior across all AI models (gpt-oss, gemma3, etc.)
  - Robust parsing of context strings with multiple format support
  - Error handling for missing or malformed template variables

## AI Settings Persistence Requirements
- **Save View Integration**: AI settings must be saved with view preferences
  - Selected AI model persistence across application sessions
  - Selected AI prompt persistence across application sessions
  - Model parameter settings persistence for each model
  - Parameter enable/disable state persistence
  - Automatic loading of AI settings on application startup
  - Integration with existing Save View functionality

## Column Management and Data Integrity Requirements
- **Comprehensive Column Support**: All Excel columns must be accessible through Column Visibility dialog
- **Complete Column Mapping**: Proper mapping between display names and Excel column names
- **Data Population Integrity**: All columns must display actual data from Excel files
- **Missing Column Detection**: Automatic detection and handling of columns missing from tree view
- **Column Order Consistency**: Tree view column order must match Excel file structure
- **Extended Column Support**: Support for all data columns including:
  - Standard ERP columns (User ERP Name, Image, SKU NR, ERP Name, KEN NAME, CAD Name, etc.)
  - Processing status columns (SN, Manually processed)
  - AI suggestion columns (SUGGESTED_CAT, SUGGESTED_SUBCAT, SUGGESTED_SUBLEVEL)
  - AI/ML status columns (AI_STATUS, USE_FOR_ML)
- **Column Visibility Fixes**: Resolved issues where columns appeared in visibility dialog but showed empty data
- **Data Extraction Verification**: Systematic testing of all columns to ensure proper data display
- **Column Count Synchronization**: Tree view structure must handle all available columns correctly

## Dependencies
- customtkinter
- pandas (for Excel file handling)
- openpyxl (for Excel file reading/writing)
- tkinter (built-in, for additional GUI components)
- requests (for Ollama API communication)
- ollama (for AI model management and text generation)
- Pillow (for image processing)
- ddgs (for web image search)
