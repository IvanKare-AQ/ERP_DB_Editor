#!/usr/bin/env python3
"""
Local build script for ERP Database Editor
This script helps with local testing of PyInstaller builds
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def get_platform_name():
    """Get the current platform name."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("Dependencies installed successfully!")

def clean_build():
    """Clean previous build artifacts."""
    print("Cleaning previous build artifacts...")
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}/")
    
    # Clean .pyc files
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                os.remove(os.path.join(root, file))
    print("Build artifacts cleaned!")

def build_executable():
    """Build the executable using PyInstaller."""
    platform_name = get_platform_name()
    print(f"Building executable for {platform_name}...")
    
    # Use the spec file for building
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "ERP_DB_Editor.spec"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        return False

def main():
    """Main build function."""
    print("ERP Database Editor - Local Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("Error: Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    install_dependencies()
    
    # Clean previous builds
    clean_build()
    
    # Build executable
    if build_executable():
        print("\n" + "=" * 50)
        print("Build completed successfully!")
        print(f"Executable location: dist/ERP_DB_Editor/")
        print(f"Platform: {get_platform_name()}")
        print("\nTo test the executable:")
        if platform.system().lower() == "windows":
            print("  cd dist/ERP_DB_Editor && ERP_DB_Editor.exe")
        else:
            print("  cd dist/ERP_DB_Editor && ./ERP_DB_Editor")
    else:
        print("\nBuild failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
