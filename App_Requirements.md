# ERP Database Editor - Requirements and Development Context
# This file contains the requirements and development context for the ERP Database Editor application

## Project Structure Requirements
- Application will have clean separation between GUI and backend elements
- GUI elements will be within src/gui folder
- Backend elements will be within src/backend folder
- src folder will contain main app and all application code
- data will contain JSON database files (tracked in git) and Images folder (ignored by git)
- GitHub repo for the project: git@github.com:IvanKare-AQ/ERP_DB_Editor.git

## UI/UX Requirements
- Modal windows will be used only when it really makes sense to reduce usage flow
- Clean and intuitive interface using CustomTkinter framework

## Initial Functional Requirements

### File Operations
- Load Database: Application automatically loads database from `data/component_database.json` on startup
- Load Categories: Application automatically loads category hierarchy from `data/airq_categories.json` on startup
- Save button to save changes to `data/component_database.json`
- No Excel file support - all data stored in JSON format

### Data Display and Navigation
- Table hierarchy is driven directly from the JSON schema:
  - `"Category"` (top level)
  - `"Subcategory"` (second level)
  - `"Sub-subcategory"` (third level)
  - Each `"ERP Name"` object is rendered under its corresponding Sub-subcategory node with no intermediate “Article …” mappings.
- Default column visibility definitions in `default_settings.json` must reference these exact JSON field names.

### Column Management
- Columns are dynamically determined from `data/component_database.json` (source of truth)
- User will be able to set visible and non-visible columns
- "Save View" button that will store column visibility settings to `config/default_settings.json`
- Column visibility settings automatically saved when changed via Column Visibility dialog
- All available columns derived from the actual JSON schema (no renaming to internal “Article …” aliases)

### Data Editing and Modification
- Right panel edit section for modifying selected ERP items
- Direct editing of the `"ERP Name"` object (`full_name`, `type`, `part_number`, `additional_parameters`)—no staging column
- Input fields populate with priority: user modifications > original JSON values
- User can modify ERP names directly and persist them to JSON
- Category, subcategory, and sub-subcategory dropdowns for item reassignment
  - Dropdowns sourced from the `data/airq_categories.json` hierarchy
  - Placeholder options ("Select Category...", etc.) only appear when a level has no available values
- "Update All Fields" button saves all field modifications (ERP Name, Manufacturer, Remark)
- "Reassign Item" button moves items to new Category/Subcategory/Sub-subcategory combinations
- All user modifications tracked in memory until saved; column names must match the JSON schema when persisting to `data/component_database.json`
- Reset actions must repopulate fields and status messages from the original JSON values (e.g., ERP Name resets use the stored `full_name`)

## Technical Requirements
- Python GUI application using CustomTkinter as GUI framework
- JSON database handling capabilities
- JSON configuration management
- Tree view implementation for hierarchical data display
- Column visibility management with persistence
- Item selection and editing functionality
- User modification tracking and persistence
- Hierarchical dropdown population and filtering
- Use virtual environment (venv) for this application

## Performance and Caching Requirements
- Initial JSON load may be slow, but all subsequent operations must work exclusively from cached pandas DataFrames (no additional disk reads until Save/Export).
- Tree view must maintain an in-memory `row_id → DataFrame index` dictionary so edit paths (reassign, update fields, delete) can locate rows in O(1) time.
- Reassigning an item should update only the impacted tree node (incremental move) and fall back to a full rebuild only when incremental updates fail.
- Filtered/modified datasets must be cached and invalidated via `_mark_data_dirty()` so editing no longer clones the full DataFrame on every keystroke.
- Added-tab drafts load lazily—`new_items.json` is touched only when the Add tab becomes active or when draft data is saved.
- All buffered edits (field updates, image changes, reassignments) must immediately refresh the UI using cached data without reloading the JSON file.

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
- Spreadsheet-style filtering functionality for columns in tree view
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
- Save functionality writes all modifications to `data/component_database.json`
- Column order is preserved from the original JSON structure
- No column renaming occurs during export or save; the exact JSON field names remain intact (only the `"ERP Name"` object is flattened when generating Excel files)
- All user modifications (ERP Name object, Manufacturer, Remark, Category/Subcategory/Sub-subcategory reassignments) are persisted to JSON
- Data enrichment: Level 3 parameters (Stage, Origin, Serialized, Usage) automatically enriched from `data/airq_categories.json`

## User Interface Requirements
- Status message bar at the bottom of the application window
- Status messages for all major operations (file operations, item selection, modifications, filters)
- File information display showing current loaded file name
- Status messages must be visible and provide clear feedback to users
- Status bar must be properly sized and positioned on application startup

## Data Integrity and Column Handling Requirements
- JSON data column names are normalized (trailing spaces removed) during loading
- Application must correctly identify and use columns from JSON structure
- All tree view operations must use consistent column references throughout the application
- Row ID generation must use the correct column name to ensure proper item identification
- Dropdown population in edit panel uses category structure from `data/airq_categories.json`
- ERP name updates must work correctly with the tree view's tag structure

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

## Data Integrity and Display Requirements
- Immediate visual updates after item reassignment operations
- Tree view must reflect user modifications in real-time without requiring file reload
- Proper handling of column name normalization (trailing spaces removed) in JSON data
- Clean JSON file output with consistent column naming during save operations
- Consistent column naming and structure throughout all operations
- User modifications must be applied to tree view data for immediate display

## Extended Field Editing Requirements
- Input fields for "ERP Name", "Manufacturer", and "REMARK" columns
- Individual reset buttons for each input field (ERP Name, Manufacturer, REMARK)
- Consolidated "Update All Fields" button to update all three fields simultaneously
- Priority system for field population: user modifications > original column values
- Real-time status updates for all field modifications
- Proper integration with save functionality to persist all field changes to JSON
- Individual field validation and error handling
- Consistent UI layout with inline reset buttons for each field


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
- **Input Field Labels**: Added descriptive labels for ERP Name, Manufacturer, and REMARK fields
- **Streamlined AI Interface**: Moved "Prompt Tool" button to AI Settings section for better organization
- **Removed Prompt Section**: Eliminated redundant prompt text area for cleaner interface
- **Enhanced Prompt Management**: "Load to Editor" functionality now works with stored prompts
- **Visual Prompt Status**: Added status label showing currently loaded prompt name
- **Improved User Experience**: Better organization and visual feedback throughout the interface

### Tabbed Interface Redesign (v1.2.0)
- **Modular Edit Panel Architecture**: Restructured right panel into three specialized tabs
  - **Editor Tab (✏️)**: Item editing, reassignment tools, image management, and new item creation (formerly Manual tab)
  - **AI Tab (🤖)**: AI-powered editing with model management and prompt tools
  - **ML Tab (🧠)**: Placeholder for future machine learning features
- **Editor Tab Functionality**: The Editor tab (formerly Manual) includes all item editing capabilities:
  - Image action buttons: `<- Add Item` (leftmost), `Import`, and `Add Image` positioned below image preview
  - `Suggest` button above `Reassign` button for category suggestions
  - All editing controls (Update All Fields, Delete Selected Item, Reassign) available in single unified interface
  - New item creation integrated directly into the editor workflow
- **Tab Switching Performance**: Tree view refresh is only triggered when switching between tabs that require different data views. Switching between Editor, AI, and ML tabs does not trigger tree view refresh, improving performance and user experience.
- **Save Button State Management**: Save button is disabled by default and only enabled when there are unsaved changes to the database, preventing accidental saves of unchanged data.
- **Reassign Button State Management**: Reassign button is disabled until category/subcategory/sub-subcategory dropdowns are changed from their original values, providing clear visual feedback on when reassignment is available.
- **View Toggle Functionality**: Toggle button in toolbar switches between "New Items" and "Current Items" views, with button label dynamically updating to reflect current view state.
- **PN Display Format**: PN (Part Number) values are displayed as 7-digit numbers with leading zeros (e.g., 0000123) throughout the application for consistent formatting.
- **Fixed Width Layout**: Right panel now uses consistent 1000px width across all tabs
- **Component Separation**: Each tab is a self-contained module with dedicated file
  - `manual_editor.py`: Manual editing functionality (ERP Name, Manufacturer, REMARK)
  - `ai_editor.py`: AI tools and model management (completely self-contained)
  - `ml_editor.py`: ML placeholder for future expansion
- **Manual Editor Streamlining**: Removed legacy data-cleaning controls that depended on Excel workflows
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
- **ERP Name Parsing System**: Advanced parsing and editing capabilities for structured naming
  - Automatic parsing of ERP Name into Type, PN (Part Number), and Details components
  - Format: Type_PN_Details (separated by underscores)
  - Bidirectional synchronization between ERP Name and parsed fields
  - Real-time updates when editing either ERP Name or individual components
  - Underscore to hyphen conversion buttons for all three fields
  - Combined conversion and update button for Details field ("_ → - + Update")
  - NO-PN quick-insert button for items without part numbers
  - Flexible naming convention support (structural _ vs descriptive - separators)
  - Visual separator between standard fields and parsed fields for clarity
- **Image Management System**: Complete image handling with web search and preview
  - Automatic Image column creation in JSON database (positioned after ERP name)
  - Image preview display (150x150) in Manual Editing tab
  - “Add Image” button located directly below the preview to keep acquisition workflow in one place
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
  - Image storage in Images/ folder alongside JSON database file
  - Configurable image settings (size, format, quality)
  - Relative path storage in JSON for portability
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
- **Dynamic Column Source**: Columns are dynamically determined from `data/component_database.json` (source of truth), with filtered views always reflecting staged modifications (reassignments, field edits) even before Save.
- **Complete Column Mapping**: Proper mapping between display names and JSON column names
- **Data Population Integrity**: All columns must display actual data from JSON database
- **Missing Column Detection**: Automatic detection and handling of columns missing from tree view
- **Column Order Consistency**: Tree view column order matches JSON file structure
- **Extended Column Support & Buffering**: Support for all data columns, with staged edits (reassignments, ERP field changes, manufacturer/remark/image updates) applied immediately in-memory while the persisted JSON remains untouched until Save. This includes:
  - Standard ERP columns (Image, SKU NR, ERP Name, KEN NAME, CAD Name, EAN13, etc.)
  - Processing status columns (PN, Manually processed)
  - Level 3 parameters (Stage, Origin, Serialized, Usage) enriched from categories
  - AI suggestion columns (SUGGESTED_CAT, SUGGESTED_SUBCAT, SUGGESTED_SUBLEVEL)
  - AI/ML status columns (AI_STATUS, USE_FOR_ML)
- **No Hardcoded Column Lists**: All column lists derived from actual data structure
- **Data Extraction Verification**: All columns display actual data from JSON database
- **Column Count Synchronization**: Tree view structure dynamically adapts to available columns

## Cross-Platform Build and Deployment Requirements
- **Automated Cross-Platform Builds**: GitHub Actions workflow for automated builds
  - Builds triggered by "#BUILD" commit message or manual dispatch
  - Support for Windows x86, Windows ARM, and macOS platforms
  - Automated release creation with platform-specific executables
  - Comprehensive PyInstaller configuration with all dependencies
  - Explicit hidden imports for all required modules
  - Proper data file handling (config, src, images)
- **macOS Compatibility**: Special handling for macOS security and permissions
  - Quarantine removal script (run_app.sh) to prevent permission prompts
  - Comprehensive README with troubleshooting instructions
  - Proper path handling for PyInstaller directory distributions
- **Font Consistency**: Consistent rendering across platforms and execution methods
  - Platform-specific theme selection for proper styling
  - Consistent font sizes (11pt) across all components
  - Dark theme styling with proper contrast
  - Tree view, AI editor, and model manager consistent styling
  - Fixed Windows column header styling (no more white-on-white text)
  - Proper font timing (fonts configured after root window creation)
- **Build Configuration**: PyInstaller with comprehensive module inclusion
  - All dependencies explicitly included as hidden imports
  - Proper SSL/certificate support for network operations
  - Config directory included in builds
  - Source directory structure preserved in builds
  - Console mode for macOS (better debugging and error visibility)

## Dependencies
- customtkinter (for GUI framework)
- pandas (for data handling and DataFrame operations)
- tkinter (built-in, for additional GUI components)
- requests (for Ollama API communication)
- ollama (for AI model management and text generation)
- Pillow (for image processing)
- ddgs (for web image search)
- pyinstaller (for cross-platform executable creation)
- Note: openpyxl removed - Excel support no longer needed
