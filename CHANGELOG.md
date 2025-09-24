# Changelog

All notable changes to the ERP Database Editor project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

## [0.1.0] - Initial Release

### Added
- Basic application framework
- File operations (open, save, save as)
- Tree view implementation
- Column visibility controls
- Configuration management
- Installation automation
