# Changelog

All notable changes to the ERP Database Editor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- **Manual Editor**: Resetting an ERP Name now reports the restored value using the correct variable, eliminating the `original_erp_name` reference error.

## [1.4.0] - 2025-11-20

### Changed
- **Database Storage**: Switched from Excel to JSON (`data/component_database.json`) for database storage
- **File Operations**: Removed "Open Excel" and "Save As" buttons; application now loads database on startup
- **Dependencies**: Removed `openpyxl` dependency as Excel is no longer used
- **Column Source**: Columns are now dynamically determined from `data/component_database.json` instead of hardcoded lists
- **Data Enrichment**: Level 3 parameters (Stage, Origin, Serialized, Usage) automatically enriched from `data/airq_categories.json`
- **Category Hierarchy**: Tree structure built from `data/airq_categories.json` instead of grouping by data columns
- **ERP Name Editing**: Removed "User ERP Name" staging column; users now edit "ERP name" directly
- **Dropdown Placeholders**: Removed "Select Category..." placeholders when actual items are available
- **ERP Name Structure**: ERP Name is now stored as an object with `full_name`, `type`, `part_number`, and `additional_parameters` properties
- **Git Tracking**: JSON database files (`component_database.json`, `airq_categories.json`) are now tracked in git; Images folder remains ignored
- **Terminology Alignment**: All internal references now use the JSON schema (`Category` / `Subcategory` / `Sub-subcategory` / `ERP Name`); the legacy “Article …” columns and `sublevel` terminology were removed
- **Export Workflow**: Added Export button next to Save and ensured Excel exports flatten only the `ERP Name.full_name` field without renaming columns

### Removed
- **User ERP Name Column**: Removed separate "User ERP Name" column - users now edit "ERP name" directly
- **Apply User ERP Names Button**: Removed button that moved User ERP Name to ERP name (no longer needed)
- **Clear User ERP Name Button**: Removed button for clearing User ERP Name (no longer needed)
- **Hardcoded Column Lists**: Removed all hardcoded column lists - columns now come from data structure
- **Rows Configuration**: Removed "rows" array from `config/default_settings.json` (columns now dynamic)

### Fixed
- **Column Visibility**: Column visibility now automatically saves to config when changed
- **ERP Name Object Handling**: Fixed ERP Name object structure preservation throughout the application
  - Tree view now displays `full_name` from ERP Name object
  - Manual editor connects to object properties (`type`, `part_number`, `additional_parameters`)
  - Update All Fields button reconstructs object structure correctly
  - Save operation preserves object structure (no restructuring to NaN)
  - Fixed pandas assignment issues by using `.at` instead of `.loc` for dict objects
  - Ensured object dtype is maintained throughout data operations
- **Dropdown Population**: Dropdowns now only show placeholders when no items are available
- **Data Source**: All column lists and dropdowns now use actual data as source of truth (no column mapping layer)

## [1.3.1] - 2025-01-XX

### Fixed
- **Build Workflow**: Resolved all platform build issues
  - Fixed Windows x86 build module imports
  - Fixed Windows ARM build module imports
  - Fixed macOS build and run script path issues
  - Fixed Ubuntu build (removed as unnecessary)
- **Release Process**: Fixed GitHub release 403 error
  - Added proper workflow-level and job-level permissions
  - Fixed token handling in release creation
  - Automated release creation now works correctly
- **Cross-Platform Compatibility**: Comprehensive fixes for all platforms
  - All platforms now build successfully
  - All platform executables are properly packaged
  - Release artifacts are correctly uploaded

## [1.3.0] - 2025-01-XX

### Added
- **Cross-Platform Executable Builds**: Automated builds for Windows x86, Windows ARM, and macOS
  - GitHub Actions workflow for automated cross-platform builds
  - Triggered by "#BUILD" commit message or manual dispatch
  - Comprehensive PyInstaller configuration with all dependencies
  - Automated release creation with platform-specific executables
  - Explicit hidden imports for all required modules (requests, customtkinter, PIL, etc.)
  - Proper SSL/certificate support for network operations
- **macOS Compatibility**: Special handling for macOS security and permissions
  - Quarantine removal script (run_app.sh) to prevent permission prompts
  - Comprehensive README with troubleshooting instructions for macOS users
  - Proper path handling for PyInstaller directory distributions
  - Console mode for better debugging and error visibility

### Changed
- **Font Consistency**: Consistent rendering across all platforms and execution methods
  - Platform-specific theme selection for proper styling
  - Consistent font sizes (11pt) across all components
  - Increased tree view row height (20 to 24) for better readability
  - Fixed font configuration timing to occur after root window creation
- **Tree View Styling**: Improved dark theme styling for Windows compatibility
  - Added platform-specific theme selection (clam or alt theme)
  - Windows compatibility styling with proper theme mapping
  - Style refresh mechanism for Windows compatibility
  - Proper column header visibility (fixed white-on-white text issue)
- **Component Styling**: Consistent dark theme across all GUI components
  - AI editor listbox styling with dark theme colors
  - Model manager dialog listbox styling with dark theme colors
  - Dark theme scrollbar styling for listboxes
  - Proper selection colors (blue selection with white text)

### Fixed
- **Tree View Column Headers**: Fixed white background with white font on Windows
  - Added platform-specific theme selection
  - Windows compatibility styling with proper theme mapping
  - Style refresh mechanism for consistent rendering
- **AI Results and Model Manager Styling**: Fixed styling issues in AI sections
  - Dark theme listbox styling with proper contrast
  - Blue selection highlighting for selected items
  - Dark theme scrollbar styling
- **macOS Permission Prompts**: Fixed permission prompts for every library
  - Added quarantine removal script (run_app.sh)
  - Comprehensive README with troubleshooting instructions
  - Proper path handling for PyInstaller directory distributions
- **Font Configuration Timing**: Fixed RuntimeError when configuring fonts too early
  - Moved font configuration to main window initialization
  - Font configuration now happens after root window creation
  - Added error handling to prevent crashes
- **macOS Run Script**: Fixed run_app.sh path issue
  - Corrected executable path inside PyInstaller directory
  - Updated README with proper instructions
  - Fixed "is a directory" error when running the script
- **GitHub Release Permissions**: Fixed 403 Forbidden error when creating releases
  - Added proper workflow-level permissions (contents: write)
  - Added job-level permissions for release creation
  - Fixed token handling to use proper token parameter
- **Build Module Imports**: Fixed missing module errors in Windows ARM builds
  - Added comprehensive hidden imports for all required modules
  - Proper SSL/certificate support
  - Config and source directory handling in PyInstaller

### Technical Improvements
- **Build Configuration**: Comprehensive PyInstaller setup
  - All dependencies explicitly included as hidden imports
  - Proper data file handling (config, src directories)
  - Platform-specific build configurations
  - Automated artifact upload and release creation

## [1.2.0] - 2025-10-13

### Added
- **Tabbed Interface Redesign**: Complete restructuring of the right panel into specialized tabs
  - **Manual Tab (✏️)**: Dedicated space for manual editing, reassignment, and data cleaning
  - **AI Tab (🤖)**: Isolated AI-powered editing with model management and prompt tools
  - **ML Tab (🧠)**: Future-ready placeholder for machine learning features
  - Professional Unicode icons for quick visual identification
  - Fixed 1000px width layout for consistent tab sizing
- **Modular Component Architecture**: Enhanced code organization and maintainability
  - Created `manual_editor.py` - self-contained manual editing module
  - Created `ai_editor.py` - self-contained AI tools module
  - Created `ml_editor.py` - placeholder ML module for future expansion
  - Created `edit_panel.py` - tabbed container orchestrating all editors
  - Each module is independently maintainable and testable
- **Unified UI Constants**: Standardized dimensions across entire application
  - Consistent button heights (35px standard, 90px for reassign button)
  - Standardized input field widths (400px)
  - Unified spacing and padding values throughout all UI files
  - Applied to all dialogs: `filter_dialog.py`, `model_manager_dialog.py`, `prompt_dialog.py`
- **Self-Contained AI Editor**: AI functionality now fully independent
  - Automatic model refresh on application startup (1000ms delay)
  - Configuration loading integrated within AI editor module
  - Independent status updates and error handling
  - No external initialization required from main window

### Changed
- **Data Cleaning Tools Relocation**: Moved buttons from toolbar to Manual tab
  - "Convert Multiline" button relocated to Manual tab bottom section
  - "Remove NEN" button relocated to Manual tab bottom section
  - Better logical grouping with other manual data operations
- **Window Sizing**: Adjusted main window dimensions to accommodate wider tabs
  - Initial geometry: 2000x1000 (increased from previous size)
  - Minimum size: 1600x800 (increased from previous minimum)
  - Right panel fixed width: 1000px for optimal content display

### Enhanced
- **Code Organization**: Improved maintainability through modular structure
  - Separation of concerns: Manual, AI, and ML functionalities isolated
  - Reduced coupling between components
  - Easier to extend and modify individual features
  - Better error isolation and debugging
- **User Experience**: Cleaner interface with logical feature grouping
  - Related tools grouped in dedicated tabs
  - Reduced visual clutter in main window
  - Intuitive tab navigation with clear icons
  - Consistent layout across all tabs

### Technical Improvements
- **Architecture**: Enhanced application structure for scalability
  - `EditPanel` acts as container for specialized editor modules
  - Each editor module is self-initializing and self-managing
  - Main window simplified to focus on orchestration
  - Reduced complexity in main_window.py (removed 200+ lines)
- **UI Framework**: Better use of CustomTkinter components
  - `CTkTabview` for professional tabbed interface
  - Proper parent-child widget hierarchy
  - Consistent styling and theming across tabs
  - Responsive layout within fixed-width container

### Fixed
- **Import References**: Corrected module imports after restructuring
  - Updated main_window.py to reference EditPanel correctly
  - Fixed attribute access chains for nested editor components
  - Added hasattr() checks for safe attribute access
- **Threading Issues**: Resolved UI update problems in AI editor
  - Changed `self.after()` to `self.main_window.root.after()` throughout ai_editor.py
  - Ensures all UI updates happen on main thread
  - Prevents potential threading exceptions
- **AI Prompt Selection Bug**: Fixed prompt not being used by Generate and Process buttons
  - Root cause: Prompt text was not stored locally when selected via Prompt Tool
  - Generate/Process buttons were reading from config file instead of current selection
  - Added `self.selected_prompt_text` to store the actual prompt text
  - Updated all AI operations (Generate, Process Selected, Process Entire Table) to use stored text
  - Fixed `load_selected_prompt_from_config()` to load both prompt name and text
  - Prompt changes now take effect immediately without requiring "Save View"
- **Item Reassignment Bug**: Fixed reassigned items losing category information
  - Root cause: `get_original_row_data()` was returning original data without applying modifications
  - Reassigned items couldn't be reassigned again due to empty/incorrect dropdown values
  - Modified `get_original_row_data()` to apply reassignment modifications to returned data
  - Now correctly applies `new_category`, `new_subcategory`, and `new_sublevel` from user modifications
  - Reassigned items can now be selected and reassigned multiple times
  - Category/subcategory/sublevel dropdowns populate correctly for reassigned items

### Added
- **User ERP Name Parsing System**: Advanced structured naming with component breakdown
  - **Automatic Parsing**: User ERP Name automatically parsed into Type, PN, and Details fields
  - **Parsing Format**: Type_PN_Details (separated by underscores)
    - Type: First component before first underscore
    - PN: Part Number between first and second underscore
    - Details: All content after second underscore
  - **Bidirectional Sync**: Real-time synchronization between User ERP Name and parsed fields
    - Editing User ERP Name updates Type, PN, Details automatically
    - Editing Type, PN, or Details reconstructs User ERP Name automatically
  - **Conversion Buttons**: Three `_ → -` buttons for underscore to hyphen conversion
    - Individual button for Type field
    - Individual button for PN field
    - Individual button for Details field
  - **NO-PN Button**: Quick-insert button for items without part numbers
    - Inserts "NO-PN" into PN field with one click
    - Automatically updates User ERP Name
    - Standardizes naming for items lacking part numbers
  - **Visual Separation**: Horizontal separator between REMARK and parsed fields for clarity
  - **Flexible Naming**: Support for mixed separator conventions
    - Structural separators: Use `_` to separate Type, PN, Details
    - Descriptive separators: Use `-` within fields for readability
  - **Smart Field Handling**: Empty fields automatically skipped when reconstructing User ERP Name
- **Image Management System**: Complete image handling with web search and local files
  - **Image Column**: Automatically created in Excel files when opening
    - Positioned after ERP name column
    - Stores relative paths to image files
    - Images saved in Images/ folder alongside Excel file
  - **Image Preview**: 150x150 pixel preview in Manual Editing tab
    - Displays current item's image
    - Shows "Multiple Items" for multi-selection
    - Shows "No Image" placeholder when no image assigned
  - **Add Image Dialog**: Modal window for image selection
    - Web image search using DuckDuckGo (no API key required)
    - Local file browser for selecting images from computer
    - PN-based automatic search (uses Part Number for web search)
    - Manual search phrase override option
    - Thumbnail grid display of search results
    - Click to select desired image
  - **Image Processing Backend** (`image_handler.py`):
    - Automatic image standardization (resize, format conversion)
    - Configurable target size (default 800x600)
    - Maintain aspect ratio option
    - PNG/JPEG format support
    - Quality settings for JPEG compression
    - Relative path management for portability
  - **Image Settings** (`images_settings.json`):
    - Configurable images folder name
    - Image format (PNG/JPEG)
    - Target dimensions (width/height)
    - Aspect ratio preservation
    - JPEG quality setting
    - Web search parameters (max results, timeout)

### Enhanced
- **Manual Editor Interface**: Improved user experience for structured naming and image management
  - Clear visual grouping of parsed components
  - Instant feedback when editing any component
  - Conversion tools for standardizing naming conventions
  - Consistent button styling across all conversion tools
  - Image preview for visual product identification
  - Streamlined button layout (Update, Add Image, Delete)
  - Left-aligned input fields for professional appearance
- **Data Persistence**: Enhanced save functionality
  - Image paths saved to Excel with user modifications
  - Relative paths ensure portability across systems
  - Images folder auto-created when needed

### Fixed
- **Image Path Resolution**: Fixed double "Images/Images/" path issue
  - Correctly handles paths with "Images/" prefix
  - Prevents path duplication when loading images
  - Smart path resolution for relative and absolute paths
- **Package Deprecation**: Updated to use new `ddgs` package
  - Added fallback support for `duckduckgo_search`
  - Eliminated deprecation warnings
  - Future-proof image search functionality

## [0.1.0] - 2024-12-19

### Added
- **Data Cleaning Functionality**: Comprehensive data cleaning tools for Excel processing
  - "Convert Multiline" button to convert multiline Excel cells to single line entries
  - "Remove NEN" button to remove "NEN" prefix and subsequent spaces from all cells
  - Automatic tree view refresh after data cleaning operations
  - Detailed statistics and progress tracking for cleaning operations
  - Confirmation dialogs for irreversible data cleaning operations
- **Enhanced AI Processing**: Improved AI-powered ERP name editing capabilities
  - Dynamic button state management (Apply → Stop processing)
  - Graceful termination of background AI processing with progress preservation
  - Real-time progress tracking with stop instructions during processing
  - Safe process termination ensuring no data loss or hanging threads
- **Improved User Experience**: Enhanced interface and workflow
  - Renamed buttons for clarity: "Process Selected" and "Process entire table"
  - Increased AI Results display height for better visibility of 5 suggestions
  - Enhanced status messages and confirmation dialogs
  - Better progress tracking and user feedback

### Removed
- **Redundant UI Elements**: Streamlined interface by removing unnecessary components
  - Removed redundant "Apply" button (functionality covered by other buttons)
  - Removed "Use entire table as context" checkbox for simplified AI operations
  - Cleaned up context selection functionality

### Fixed
- **AI Processing Control**: Improved thread management and process control
  - Fixed potential hanging threads during AI processing
  - Ensured clean termination of background processes
  - Improved button state synchronization during processing
  - Fixed tree view update issues after data cleaning operations
- **Data Display and Integrity Issues**: Fixed critical display and save operation problems
  - Fixed tree view not updating immediately after item reassignment operations
  - Fixed "Save As" creating duplicate "Article Sublevel" columns in Excel files
  - Fixed user modifications not being applied to tree view data for real-time display
  - Fixed duplicate column handling with trailing spaces in Excel data processing
  - Improved column cleanup logic to properly identify and remove duplicate columns
- **Apply User ERP Names Functionality**: Fixed detection and processing of existing User ERP Name values
  - Fixed "Apply User ERP Names" button to detect User ERP Name values from original Excel data
  - Previously only checked user modifications, now checks both user modifications and original data
  - Proper handling of Excel files that already contain "User ERP Name" column with values
  - Accurate count display in confirmation dialog for all available User ERP Names
  - Fixed double counting bug in confirmation dialog when user modifications exist alongside original data
  - Implemented unique row tracking to prevent counting the same User ERP Name multiple times

## [Unreleased]

## [1.2.1] - 2025-10-21

### Fixed
- **Image Download Reliability**: Enhanced image downloading with robust URL handling
  - Added URL normalization with multiple retry strategies for failed downloads
  - Automatic handling of URL encoding variations (spaces, `+` characters, special chars)
  - Support for case-insensitive file extensions (`.jpg` vs `.JPG`)
  - Intelligent retry logic that tries multiple URL formats before failing
  - Enhanced error messages with specific reasons and helpful tips for users
  - Better handling of 404 (Not Found), 403 (Forbidden), timeout, and connection errors
  - Examples: Handles DigiKey URLs with spaces like `Assmann+Photos/AHDS15A-KG-TAXB-R.JPG`
- **Local Image Preview**: Complete preview functionality for local file selection
  - Full image preview (up to 400x400) when selecting local files
  - Detailed file information display (filename, dimensions, format, size)
  - Visual highlighting of selected image with blue frame
  - Loading status with thread-safe UI updates
  - Proper error handling with informative messages
  - Added `.webp` to supported image formats
- **Column Visibility Dialog**: Fixed critical bug preventing access to hidden columns
  - Root cause: Dialog was reading from tree's current columns instead of master list
  - Added permanent master column list (`all_columns`) that never changes
  - Added `get_all_columns()` method to tree view widget
  - Dialog now always shows all 16 available columns regardless of current visibility
  - Users can now freely hide and show columns without losing access
  - Fixed column visibility restoration from saved settings

### Enhanced
- **Image Handler** (`image_handler.py`):
  - Smarter URL parsing with multiple format attempts
  - Progressive retry strategy for unreliable image URLs
  - Better user feedback with progress messages during retries
  - Import of `urllib.parse` for robust URL handling
- **Image Selection Dialog** (`image_dialog.py`):
  - Professional preview display with proper sizing
  - File metadata display (dimensions, format, size in KB/MB)
  - Thread-safe loading for responsive UI
  - Added `os` module to imports for file operations
- **Tree View Widget** (`tree_view.py`):
  - Cleaner architecture with separation of column management
  - Master column list ensures consistent column availability
  - Better method naming with `get_all_columns()` vs `get_visible_columns()`

### Technical Improvements
- **URL Processing**: Added sophisticated URL normalization algorithm
  - Decodes and re-encodes URLs to handle various formats
  - Tests multiple URL variations (original, encoded, case variations)
  - Prevents wasted attempts on 403 errors (blocked by website)
  - Continues trying alternatives for 404 errors (might work with different format)
- **UI Architecture**: Enhanced column management system
  - Immutable master column list prevents state corruption
  - Clear separation between available and visible columns
  - Proper getter methods for different column access patterns

## [1.2.3] - 2025-01-27

### Added
- **Combined Conversion and Update Button**: Enhanced Details field functionality
  - Added "_ → - + Update" button next to existing "_ → -" button in Details field
  - Combines underscore-to-hyphen conversion with "Update All Fields" functionality
  - Single-click operation for efficient workflow
  - Streamlined user experience for frequent conversion and update operations

### Enhanced
- **User ERP Name Parsing System**: Improved workflow efficiency
  - Combined button provides one-click solution for conversion and field updates
  - Maintains existing individual button functionality for granular control
  - Better user experience for users who frequently need both operations

## [1.2.2] - 2025-01-27

### Fixed
- **Column Visibility Data Display**: Comprehensive fix for empty column data issue
  - **Root Cause**: Missing cases in `populate_tree_with_visibility()` method for several columns
  - **KEN NAME Column**: Fixed missing case that caused empty data display despite column being visible
  - **Extended Column Support**: Added support for all missing Excel columns:
    - SN (Serial Number)
    - Manually processed (Processing status)
    - SUGGESTED_CAT, SUGGESTED_SUBCAT, SUGGESTED_SUBLEVEL (AI suggestions)
    - AI_STATUS, USE_FOR_ML (AI/ML status columns)
  - **Column Order Consistency**: Updated column order to match Excel file structure
  - **Data Population Integrity**: All 24 columns now display actual data from Excel files
  - **Systematic Testing**: Verified all columns work correctly with comprehensive testing

### Enhanced
- **Column Management System**: Complete overhaul of column handling
  - **Master Column List**: Updated from 17 to 24 columns to include all Excel columns
  - **Column Mapping**: Added proper mapping for all new columns in `get_data_column_name()`
  - **Data Extraction**: Updated `populate_tree_with_visibility()` to handle all column types
  - **Tree Structure**: Updated hardcoded empty string tuples to match new column count
  - **Column Visibility Dialog**: Now includes all available columns for proper visibility management

### Technical Improvements
- **Data Integrity**: Systematic verification of all column data extraction
- **Column Synchronization**: Tree view structure now handles all available columns correctly
- **Missing Column Detection**: Automatic detection and handling of columns missing from tree view
- **Column Order Validation**: Ensured tree view column order matches Excel file structure

### Added
- **Comprehensive Column Support**: Full support for all Excel file columns
  - Standard ERP columns: User ERP Name, Image, SKU NR, ERP Name, KEN NAME, CAD Name, etc.
  - Processing status columns: SN, Manually processed
  - AI suggestion columns: SUGGESTED_CAT, SUGGESTED_SUBCAT, SUGGESTED_SUBLEVEL
  - AI/ML status columns: AI_STATUS, USE_FOR_ML
- **Data Verification**: Systematic testing framework for column data integrity
- **Column Count Synchronization**: Proper handling of all 24 columns in tree view structure

## [Unreleased]

### Added
- **AI Model Management System**: Complete model management functionality
  - Model Manager dialog (900x700) for downloading, removing, and configuring AI models
  - Dynamic parameter display based on model capabilities using `ollama show` command
  - Model parameter tuning with sliders, input fields, and checkboxes
  - Parameter enable/disable functionality with persistent settings
  - Model-specific parameter storage in configuration file
  - Real-time parameter validation and type conversion (int, float, str)
  - Bidirectional synchronization between sliders and input fields
  - Model information display (architecture, parameters, context length, quantization)
  - Automatic parameter initialization for new models based on model type
  - Robust error handling for model operations and parameter management
- **AI Prompt Template System**: Automatic template variable substitution
  - Support for `{erp_name}`, `{category}`, `{subcategory}`, `{sublevel}` variables
  - Automatic extraction of ERP item data from context strings
  - Template substitution before sending prompts to AI models
  - Consistent behavior across all AI models (gpt-oss, gemma3, etc.)
  - Robust parsing of context strings with multiple format support
  - Error handling for missing or malformed template variables
- **AI Settings Persistence**: Integration with Save View functionality
  - Selected AI model persistence across application sessions
  - Selected AI prompt persistence across application sessions
  - Model parameter settings persistence for each model
  - Parameter enable/disable state persistence
  - Automatic loading of AI settings on application startup
  - Integration with existing Save View functionality
- **Enhanced Model Manager Interface**: Professional model management UI
  - Two-panel layout (left for model list/actions, right for parameters)
  - Model list with download and remove functionality
  - Parameter tuning section with dynamic widget creation
  - Save button state management for parameter changes
  - Real-time parameter validation and type conversion
  - Model information display with detailed specifications
  - Automatic parameter initialization for new models
  - Robust error handling for model operations

### Fixed
- **AI Prompt Template Substitution**: Fixed critical issue where AI models received unsubstituted template variables
  - Root cause: Prompt templates contained variables like `{erp_name}`, `{category}` that were not being replaced
  - Added `_extract_erp_data_from_context()` method to parse context strings and extract ERP item data
  - Implemented template variable substitution in `generate_erp_names()` method
  - Fixed gpt-oss model receiving raw template variables instead of actual ERP item data
  - Ensured consistent behavior across all AI models (gpt-oss, gemma3, etc.)
  - Added robust parsing of context strings with multiple format support
  - Implemented error handling for missing or malformed template variables
- **Model Manager Dialog Issues**: Fixed multiple critical issues in model management
  - Fixed `KeyError: 'widget'` in `update_parameter_enabled` method for text parameters
  - Fixed Save button graying out when clicking on input fields
  - Fixed parameter reset to default values when re-selecting the same model
  - Replaced problematic `<<ListboxSelect>>` event binding with specific event handlers
  - Added `on_model_click()` and `on_model_key_select()` methods for better event handling
  - Implemented `check_model_selection()` with delayed processing to prevent focus issues
  - Fixed parameter preservation when selecting the same model multiple times
  - Added `update_parameter_values_from_config()` to refresh UI without recreating widgets
  - Enhanced Save button state management to remain enabled during parameter changes
- **Parameter Type Conversion**: Fixed parameter type handling in model management
  - Fixed `num_ctx` (context length) being saved as float instead of integer
  - Fixed floating point precision issues (e.g., 0.20 saving as "0.19999999999999996")
  - Implemented proper type conversion (int, float, str) when saving parameters
  - Added rounding logic for float values based on step values
  - Enhanced parameter validation and error handling
- **Model Parameter Persistence**: Fixed parameter saving and loading issues
  - Fixed new models not getting parameters saved in settings file
  - Implemented `_initialize_new_model_parameters()` for automatic parameter creation
  - Enhanced `get_model_parameters()` to automatically create default parameters for new models
  - Fixed parameter reset issues when selecting models
  - Added proper parameter type conversion and validation
  - Implemented robust error handling for parameter operations

### Enhanced
- **AI Model Integration**: Improved AI model handling and parameter management
  - Dynamic parameter display based on model capabilities
  - Model-specific parameter storage and retrieval
  - Automatic parameter initialization for new models
  - Enhanced parameter validation and type conversion
  - Improved error handling for model operations
  - Better user feedback and status updates
- **User Interface**: Enhanced model management interface
  - Professional two-panel layout for model management
  - Dynamic parameter widgets based on model capabilities
  - Real-time parameter validation and type conversion
  - Bidirectional synchronization between sliders and input fields
  - Improved Save button state management
  - Better error handling and user feedback
- **Parameter Management**: Enhanced parameter handling and persistence
  - Parameter enable/disable functionality with persistent settings
  - Model-specific parameter storage in configuration file
  - Real-time parameter validation and type conversion
  - Automatic parameter initialization for new models
  - Robust error handling for parameter operations
  - Better user feedback and status updates

### Added
- **Item Deletion Functionality**: Complete item removal system
  - Added "Delete Selected Item" button under "Edit Selected Item" section
  - Red color scheme to indicate destructive action
  - Confirmation dialog with detailed item information before deletion
  - Proper cleanup of user modifications and data removal
  - Real-time tree view updates after deletion
  - Status feedback for successful deletion operations
- **Input Field Labels**: Enhanced edit panel with descriptive labels
  - Added "User ERP Name:" label for ERP name input field
  - Added "Manufacturer:" label for manufacturer input field
  - Added "REMARK:" label for remark input field
  - Consistent styling with bold font and proper spacing
  - Improved user experience with clear field identification
- **Streamlined AI Interface**: Reorganized AI functionality for better workflow
  - Moved "Prompt Tool" button from removed Prompt section to AI Settings
  - Renamed "Select Prompt" to "Prompt Tool" for clarity
  - Integrated prompt tool with other AI Settings controls
  - Removed redundant Prompt section for cleaner interface
- **Enhanced Prompt Management**: Improved prompt selection and usage
  - Fixed "Load to Editor" functionality after prompt section removal
  - Added prompt storage system for AI operations
  - Visual status label showing currently loaded prompt name
  - Proper fallback to default prompt when none selected
  - Enhanced user feedback with prompt name display

### Fixed
- **Excel File Loading Issue**: Resolved "Failed to load file: 'Article Sublevel '" error
  - Root cause: Inconsistent column name handling throughout codebase
  - Some parts used 'Article Sublevel ' (with trailing space), others used 'Article Sublevel' (without space)
  - Standardized all column references to use 'Article Sublevel' (without trailing space)
  - Fixed in files: excel_handler.py, edit_panel.py, tree_view.py, main_window.py
  - Excel files now load properly without column name mismatch errors
- **Prompt Management Workflow**: Fixed "Load to Editor" functionality
  - Resolved issue where removing prompt text area broke prompt loading
  - Implemented proper prompt storage and retrieval system
  - Updated AI operations to use stored prompts instead of default
  - Enhanced visual feedback with prompt name display
  - Maintained backward compatibility with existing functionality

### Added
- **Extended Field Editing**: Enhanced edit panel with additional input fields
  - Added "Manufacturer" input field with individual reset functionality
  - Added "REMARK" input field with individual reset functionality
  - Consolidated "Update All Fields" button to update all three fields simultaneously
  - Individual reset buttons for User ERP Name, Manufacturer, and REMARK fields
  - Priority-based field population (user modifications > original values)
  - Real-time status updates for all field modifications
  - Proper integration with save functionality to persist all field changes
- **User ERP Name Application**: Permanent move operation for User ERP Names
  - Added "Apply User ERP Names" button to toolbar for permanent value transfer
  - Destructive operation that moves User ERP Name values to ERP name column
  - Replaces existing ERP name values with User ERP Name values
  - Clears User ERP Name column after successful application
  - Confirmation dialog with clear warning about permanent nature
  - Real-time count display of available User ERP Names for application
  - Immediate tree view update to reflect changes
  - Comprehensive error handling and status feedback
  - Supports both user modifications and existing User ERP Name values from Excel files
- **AI Prompt Management System**: Complete prompt storage and selection functionality
  - Added "Save Prompt" and "Select Prompt" buttons to AI Settings section
  - Dynamic button state management based on prompt content
  - Save Prompt button disabled when prompt field is empty, enabled when content exists
  - Prompt selection dialog with two-panel layout (prompt list + preview)
  - Left panel displays prompt names and descriptions for easy browsing
  - Right panel shows full prompt text preview for detailed review
  - Prompt deletion functionality with confirmation dialogs
  - JSON-based prompt storage in config/prompts.json file
  - Git integration for prompt file version control and sharing
  - Prompt overwrite protection with user confirmation
  - Real-time status updates for all prompt operations
  - Example prompts included for common ERP naming tasks
  - Enhanced prompt selection dialog with additional management features
  - Load to Editor functionality within selection dialog for modified prompts
  - Edit Description functionality with simple dialog for quick description updates
  - Duplicate functionality to create copies of prompts with " - Copy" suffix
  - Rename Prompt functionality with name and description editing
  - Increased dialog height (800x700) to accommodate all management buttons
  - Prompt modification capabilities without leaving selection dialog
  - Clear separation between prompt loading (Select AI Prompt dialog) and prompt saving (main application)
  - Visual highlighting of selected prompts with subtle gray colors for better user experience
  - Streamlined interface with Load to Editor as primary selection method
  - Improved user workflow for prompt management and editing
  - Fixed SavePromptDialog variable reference errors for proper initialization
  - Fixed button reference errors in prompt dialog after interface updates
  - Ensured Save button is properly configured in Save AI Prompt dialog
  - Increased Save AI Prompt dialog size (700x600) for better visibility
  - Enhanced Save and Cancel button styling with larger size and bold fonts
  - Improved button layout with proper spacing and padding for better user experience
  - Reduced button sizes in Select AI Prompt dialog to accommodate new Duplicate button
  - Added Duplicate button with smart naming (adds " - Copy" suffix and handles conflicts)
  - Enhanced button state management for all prompt operations
  - Improved user experience with compact, professional interface design
  - Removed Edit Description button for streamlined interface
  - Renamed Rename Prompt to Edit Prompt for clarity
  - Made Prompt Preview read-only for safe viewing
  - Enhanced Edit Prompt window with full text editing capability
  - Standardized Save Prompt button naming across create/edit modes
  - Fixed AI context parsing to include complete ERP item information
  - Enhanced AI processing with proper category, subcategory, and sublevel context
  - Improved AI suggestion accuracy through complete data context

## [0.1.1] - 2024-12-19

### Added
- **AI Prompt Management System**: Complete prompt management functionality
  - Save Prompt button in main application for creating new prompts
  - Select AI Prompt dialog with comprehensive management features
  - Load to Editor functionality for quick prompt loading
  - Edit Description functionality with simple dialog interface
  - Duplicate functionality with intelligent naming system
  - Rename Prompt functionality with full name/description editing
  - Delete Prompt functionality with confirmation dialogs
  - Visual highlighting of selected prompts with subtle gray colors
  - Smart duplicate naming with conflict resolution (" - Copy", " - Copy (1)", etc.)

### Enhanced
- **User Interface Improvements**:
  - Subtle gray highlighting instead of aggressive blue colors
  - Compact button layout with optimized sizing (100x30px for most buttons, 80x30px for Duplicate)
  - Increased Save AI Prompt dialog size (700x600) for better visibility
  - Enhanced Save and Cancel button styling with larger size and bold fonts
  - Professional color scheme throughout the application
  - Improved button state management and user feedback

### Fixed
- **Bug Fixes**:
  - Fixed SavePromptDialog variable reference errors for proper initialization
  - Fixed button reference errors in prompt dialog after interface updates
  - Ensured Save button is properly configured and visible in Save AI Prompt dialog
  - Resolved persistent method reference issues in prompt dialog
  - Fixed button state management across all prompt operations

### Technical Improvements
- **Code Quality**:
  - Enhanced error handling for prompt operations
  - Improved button state management across all dialogs
  - Better separation of concerns between prompt creation and management
  - Streamlined user workflow for prompt operations
  - Consistent styling and behavior across all UI components

### Interface Refinements
- **Streamlined Button Interface**: Removed redundant Edit Description button
- **Clear Functionality Separation**: Read-only preview vs. editable edit window
- **Enhanced Editing Experience**: Full text editing capability in Edit Prompt window
- **Consistent Naming**: Standardized "Save Prompt" button across create/edit modes
- **Improved User Safety**: Read-only prompt preview prevents accidental editing
- **Better Workflow**: Clear distinction between viewing and editing modes

## [1.0.0] - 2024-12-19

### 🎉 Major Release - Production Ready

This is the first major release of the ERP Database Editor, marking the transition from development to production-ready software.

### Fixed
- **AI Context Processing**: Resolved critical issue where AI was receiving placeholder text instead of actual ERP item data
  - Fixed "Process Selected" functionality to provide complete context (ERP name, category, subcategory, sublevel)
  - Fixed "Process entire table" functionality with proper context generation
  - Enhanced preview generation with complete item information
  - Eliminated placeholder text like `{erp_name}`, `{category}`, `{subcategory}`, `{sublevel}` in AI responses

### Enhanced
- **AI Processing Accuracy**: Complete ERP item context now provided to AI for all operations
  - Process Selected: Full context for each selected item
  - Process entire table: Full context for all table items
  - Preview generation: Complete item hierarchy information
  - Better AI suggestions through comprehensive data context

### Technical Improvements
- **Context Generation**: Enhanced context generation across all AI processing functions
- **Data Integrity**: Ensured all required ERP fields are properly extracted and passed to AI
- **Error Prevention**: Eliminated AI processing errors caused by incomplete context data
- **Consistent Behavior**: Unified context generation across all AI operations

### Production Features
- **Complete ERP Management**: Full-featured ERP database editing capabilities
- **AI-Powered Processing**: Advanced AI integration with Ollama for intelligent ERP name generation
- **Comprehensive Data Handling**: Support for Excel files with hierarchical ERP data structure
- **Professional User Interface**: Modern, intuitive GUI with CustomTkinter
- **Advanced Filtering**: Excel-style filtering with multiple criteria support
- **Column Management**: Dynamic column visibility and ordering
- **Data Validation**: Robust error handling and data integrity checks
- **Multi-selection Support**: Efficient bulk operations with Shift/Ctrl key support
- **Prompt Management**: Complete AI prompt save/load/edit/duplicate system
- **Real-time Processing**: Background AI operations with stop functionality
- **Status Feedback**: Comprehensive status updates and progress tracking

### System Requirements
- Python 3.8+
- CustomTkinter for modern GUI
- Pandas and OpenPyXL for Excel processing
- Requests for AI integration
- Ollama for AI model management

### Installation
```bash
git clone <repository>
cd ERP_DB_Editor
./install.sh  # Linux/macOS
# or
install.bat   # Windows
source venv/bin/activate
python src/main.py
```

- **Stop Processing Functionality**: Dynamic button state management for AI operations
  - Buttons convert to "Stop processing" during AI operations
  - Users can cancel long-running AI operations at any time
  - Graceful termination with progress preservation
  - Real-time progress tracking with stop instructions
  - Safe process termination ensuring no data loss or hanging threads
- **Enhanced AI Results Display**: Increased AI Results listbox height from 4 to 6 rows for better visibility of 5 suggestions
- **Improved User Experience**: 
  - Confirmation dialogs now mention ability to stop processing
  - Status messages provide clear stop instructions during processing
  - Progress tracking shows exact number of items processed before stopping

### Removed
- **Context Selection Checkbox**: Removed "Use entire table as context" checkbox and related functionality
  - Simplified AI context handling to always use selected item context
  - Removed `update_context_info()` and `get_entire_table_context()` methods
  - Streamlined AI generation to focus on individual item context

### Fixed
- **AI Processing Control**: Implemented proper thread management for AI operations
  - Fixed potential hanging threads during AI processing
  - Ensured clean termination of background processes
  - Improved button state synchronization during processing

### Added
- Initial project structure with clean architecture
- CustomTkinter-based GUI framework
- Excel file handling capabilities (open, save, save as)
- Hierarchical tree view with Article Category → Article Subcategory → Article Sublevel → ERP Names structure
- Column visibility management with persistence
- Configuration management using JSON
- Virtual environment support
- Automated installation scripts for Linux/macOS and Windows
- Project documentation (README.md, App_Requirements.md)
- Installation verification script

### Fixed
- Fixed backend path references in test_installation.py (src/backend/ instead of backend/)
- Improved error handling in test script with better messages for missing modules
- Enhanced installation scripts to handle test failures gracefully
- Test script now correctly identifies project structure and missing dependencies
- Fixed column visibility functionality - changes now properly reflected in table view
- Implemented proper column hiding/showing in tree view widget
- Added column visibility loading from configuration on startup
- Removed modal success messages from file operations for better user experience
- Fixed column visibility dialog to show all available columns
- Implemented dynamic tree view recreation with only visible columns
- Added proper column mapping for visible columns only
- Fixed column visibility workflow bug - Apply button now only updates view temporarily
- Added Save View button state management - grays out when no changes exist
- Implemented proper separation between temporary view changes and persistent settings

### Added
- Excel-style filtering functionality for tree view columns
- Filter dialog with individual column filter controls
- Multiple filter types: contains, equals, starts with, ends with
- Filter toolbar buttons: Filter Data and Clear Filters
- Real-time filter application with immediate tree view updates
- Integration with column visibility settings
- Hierarchical tree structure preservation during filtering
- Filter settings persistence with Save View functionality
- Automatic filter loading from settings file on application startup
- Filter state synchronization with Save View button management

### Fixed
- Fixed filter loading timing - filters now load after data is available
- Fixed Save View button state updates when filters are changed
- Fixed filter persistence and restoration functionality

### Added
- User ERP Name column for editing ERP item names
- Right panel edit section with input field and dropdowns
- Item selection functionality with proper data population
- Category, subcategory, and sublevel dropdowns for reassignment
- User modification tracking system for changes before save
- Hierarchical dropdown population based on data relationships
- Item reassignment functionality with category/subcategory/sublevel changes
- Enhanced save functionality to apply all user modifications

### Fixed
- Fixed item selection to only respond to ERP items (not hierarchy nodes)
- Fixed row ID generation to handle duplicate Article Sublevel columns
- Fixed column visibility to respect saved settings properly
- Fixed data mapping issues between display columns and source data
- Fixed edit panel population with correct ERP names and dropdown values
- Fixed duplicate column handling in Excel data loading
- Fixed User ERP Name column visibility based on settings
- Fixed "User ERP Name" column positioning in Excel save files (now appears after "ERP name" column)
- Fixed column reordering to preserve data during save operations

### Added
- Status message bar at bottom of application window
- Status messages for file operations (open, save, save as)
- Status messages for item operations (selection, name updates, reassignment)
- Status messages for filter operations (open dialog, clear filters)
- File information display showing current loaded file name
- Comprehensive user feedback for all major operations
- Smart column reordering logic for consistent Excel file structure
- AI-powered ERP name editing with Ollama integration
- Model management (refresh, download) for AI functionality
- AI prompt input with context selection (entire table vs selected item)
- AI-generated preview suggestions for ERP names
- Threading support for non-blocking AI operations

### Fixed
- Fixed duplicate "Article Sublevel" column issue in save operations
- Fixed "User ERP Name" column population from existing Excel data
- Fixed edit panel input field to use priority: user modifications > existing "User ERP Name" > "ERP name"
- Fixed column cleanup during save operations (keep only first occurrence of duplicate columns)
- Fixed application startup issues with CTkTextbox parameter compatibility
- Fixed status bar initialization order to prevent AttributeError
- Fixed Ollama integration with proper error handling and status updates

### Technical
- Backend components moved under src/backend/ for better organization
- Clean separation between GUI and backend layers
- Modular architecture with dedicated packages
- Comprehensive error handling
- Cross-platform installation support

### Documentation
- README.md with installation and usage instructions
- App_Requirements.md with project requirements and development context
- Installation scripts with colored output and error handling
- Project structure documentation
- **Dark Mode Theme**: Implemented dark mode styling for the table view
  - Dark background (#2b2b2b) with white text for better readability
  - Dark header background (#3c3c3c) with white text
  - Alternating row backgrounds for ERP items:
    - Even rows: Dark background (#2b2b2b)
    - Odd rows: Slightly lighter dark background (#333333)
  - Color-coded hierarchy levels with dark theme:
    - Categories: Dark gray background (#404040) with light blue text (#64b5f6)
    - Subcategories: Medium dark gray background (#4a4a4a) with light purple text (#ba68c8)
    - Sublevels: Lighter dark gray background (#545454) with light green text (#81c784)
  - Dark theme hover effects (#424242) and selection highlighting (#1976d2)

### Fixed
- **Article Sublevel Display**: Fixed missing Article Sublevel in tree hierarchy
  - Root cause: Excel data contains 'Article Sublevel ' (with trailing space) but code was looking for 'Article Sublevel' (without space)
  - Updated all tree view operations to use correct column name consistently
  - Fixed row ID generation, dropdown population, and data processing methods
- **User ERP Name Updates**: Fixed User ERP Name not updating after dark mode implementation
  - Updated tree selection handler to recognize new alternating row tag names (erp_item_even, erp_item_odd)
  - Maintained compatibility with existing tag structure while supporting new styling
- **Sublevel Dropdown Population**: Fixed Sublevel dropdown not updating on item selection in Reassign Item section
  - Updated set_selected_item method to use correct column name ('Article Sublevel ' with trailing space)
  - Now all three dropdowns (Category, Subcategory, Sublevel) populate correctly when items are selected
- **AI Generation Functionality**: Fixed AI generation not working properly
  - Fixed UI update calls from background threads using self.main_window.root.after()
  - Changed Generate button initial state from "disabled" to "normal"
  - Improved error handling and user feedback for AI operations
- **Item Selection Issues**: Fixed item selection not working with AI generation
  - Root cause: Row ID delimiter collision with ERP names containing underscores and pipes
  - Implemented robust Unicode delimiter (◆◆◆) that's virtually guaranteed to be unique
  - Updated all row ID generation and parsing to use new delimiter
  - Fixed IndentationError in tree_view.py that was preventing application startup
  - Enhanced AI generation to work with both single and multiple item selections

## [0.1.0] - Initial Release

### Added
- Basic application framework
- File operations (open, save, save as)
- Tree view implementation
- Column visibility controls
- Configuration management
- Installation automation
