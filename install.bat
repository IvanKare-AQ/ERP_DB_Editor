@echo off
REM ERP Database Editor - Installation Script for Windows
REM This script automates the installation process for the ERP Database Editor

echo ==========================================
echo ERP Database Editor - Installation Script
echo ==========================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [SUCCESS] Python found
echo.

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created
echo.

REM Activate virtual environment and install packages
echo [INFO] Activating virtual environment and installing packages...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo [INFO] Installing required packages...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages
    pause
    exit /b 1
)
echo [SUCCESS] All packages installed successfully
echo.

REM Create data directory
echo [INFO] Creating necessary directories...
if not exist data mkdir data
echo [SUCCESS] Directories created
echo.

REM Verify installation
echo [INFO] Verifying installation...
if exist test_installation.py (
    echo [INFO] Running installation test...
    python test_installation.py
    if %errorlevel% neq 0 (
        echo [WARNING] Installation test failed, but installation may still be successful
    ) else (
        echo [SUCCESS] Installation verification completed
    )
) else (
    echo [WARNING] Test script not found, skipping verification
)
echo.

echo [SUCCESS] Installation completed successfully!
echo.
echo To run the application:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Run the application:
echo    python src\main.py
echo.
echo To deactivate the virtual environment:
echo    deactivate
echo.
pause
