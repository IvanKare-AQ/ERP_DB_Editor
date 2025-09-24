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
