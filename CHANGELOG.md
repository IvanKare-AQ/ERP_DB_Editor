# Changelog

All notable changes to the ERP Database Editor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
