#!/usr/bin/env python3
"""
Test script to verify ERP Database Editor installation
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    required_modules = [
        'customtkinter',
        'pandas', 
        'openpyxl',
        'tkinter'
    ]
    
    print("Testing required module imports...")
    
    failed_modules = []
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} - OK")
        except ImportError as e:
            print(f"✗ {module} - FAILED: {e}")
            failed_modules.append(module)
    
    if failed_modules:
        print(f"\n[INFO] {len(failed_modules)} module(s) not installed: {', '.join(failed_modules)}")
        print("[INFO] Run 'pip install -r requirements.txt' to install missing modules")
        return False
    
    return True

def test_project_structure():
    """Test if project structure is correct."""
    import os
    
    required_files = [
        'src/main.py',
        'src/gui/main_window.py',
        'src/gui/tree_view.py', 
        'src/gui/column_visibility.py',
        'src/backend/excel_handler.py',
        'src/backend/config_manager.py',
        'config/default_settings.json'
    ]
    
    print("\nTesting project structure...")
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} - OK")
        else:
            print(f"✗ {file_path} - MISSING")
            return False
    
    return True

def main():
    """Main test function."""
    print("ERP Database Editor - Installation Test")
    print("=" * 40)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test project structure
    structure_ok = test_project_structure()
    
    print("\n" + "=" * 40)
    if imports_ok and structure_ok:
        print("✓ All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("python src/main.py")
    else:
        print("✗ Some tests failed. Please check the installation.")
        sys.exit(1)

if __name__ == "__main__":
    main()
