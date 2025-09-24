#!/bin/bash

# ERP Database Editor - Installation Script
# This script automates the installation process for the ERP Database Editor

set -e  # Exit on any error

echo "=========================================="
echo "ERP Database Editor - Installation Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    
    # Check Python version
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ -d "venv" ]; then
        print_warning "Virtual environment already exists. Removing old one..."
        rm -rf venv
    fi
    
    $PYTHON_CMD -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment and install packages
install_packages() {
    print_status "Activating virtual environment and installing packages..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_status "Upgrading pip..."
    pip install --upgrade pip
    
    # Install requirements
    print_status "Installing required packages..."
    pip install -r requirements.txt
    
    print_success "All packages installed successfully"
}

# Verify installation
verify_installation() {
    print_status "Verifying installation..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Run test script
    if [ -f "test_installation.py" ]; then
        print_status "Running installation test..."
        if python test_installation.py; then
            print_success "Installation verification completed"
        else
            print_warning "Some tests failed, but installation may still be successful"
        fi
    else
        print_warning "Test script not found, skipping verification"
    fi
}

# Create data directory
create_directories() {
    print_status "Creating necessary directories..."
    
    mkdir -p data
    print_success "Directories created"
}

# Main installation process
main() {
    echo
    print_status "Starting ERP Database Editor installation..."
    echo
    
    # Check Python
    check_python
    
    # Create virtual environment
    create_venv
    
    # Install packages
    install_packages
    
    # Create directories
    create_directories
    
    # Verify installation
    verify_installation
    
    echo
    print_success "Installation completed successfully!"
    echo
    echo "To run the application:"
    echo "1. Activate the virtual environment:"
    echo "   source venv/bin/activate"
    echo
    echo "2. Run the application:"
    echo "   python src/main.py"
    echo
    echo "To deactivate the virtual environment:"
    echo "   deactivate"
    echo
}

# Run main function
main "$@"
