#!/bin/bash

# Build script for FabriCalc Linux executable

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if file exists
file_exists() {
    [ -f "$1" ]
}

print_status "Starting FabriCalc build process..."

# Check if Python is installed
if ! command_exists python3; then
    print_error "Python 3 is not installed or not in PATH"
    print_error "Please install Python 3 and try again"
    exit 1
fi

# Check if pip is installed
if ! command_exists pip; then
    print_error "pip is not installed or not in PATH"
    print_error "Please install pip and try again"
    exit 1
fi

# Check if main.py exists
if ! file_exists "main.py"; then
    print_error "main.py not found in current directory"
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check if config.json exists
if ! file_exists "config.json"; then
    print_warning "config.json not found, will create default configuration"
    # Create default config if it doesn't exist
    cat > config.json << EOF
{
  "materiales": {
    "PLA Wood": 150000.0,
    "PETG": 120000.0,
    "PLA+": 90000.0
  },
  "electricidad_kwh": 968.0,
  "consumo_kw_por_hora": 0.5,
  "precio_impresora": 1200000.0,
  "vida_util_horas": 1000.0,
  "envio_local": 6000.0,
  "envio_nacional": 12000.0,
  "precio_hora_trabajo": 6741.0,
  "factor_desperdicio": 100.0,
  "tiempo_calentamiento": 10.0
}
EOF
    print_status "Created default config.json"
fi

print_status "Installing PyInstaller..."

# Install PyInstaller with error handling
if ! pip install pyinstaller; then
    print_error "Failed to install PyInstaller"
    print_error "Please check your internet connection and try again"
    exit 1
fi

print_status "PyInstaller installed successfully"

# Clean previous builds
if [ -d "dist" ]; then
    print_status "Cleaning previous build..."
    rm -rf dist
fi

if [ -d "build" ]; then
    print_status "Cleaning build cache..."
    rm -rf build
fi

if [ -f "FabriCalc.spec" ]; then
    print_status "Removing old spec file..."
    rm -f FabriCalc.spec
fi

print_status "Creating executable..."

# Create the executable with error handling
if pyinstaller --onefile \
               --windowed \
               --name FabriCalc \
               --add-data "config.json:." \
               main.py; then
    
    print_status "Build completed successfully!"
    
    # Check if executable was created
    if file_exists "dist/FabriCalc"; then
        print_status "Executable location: dist/FabriCalc"
        print_status "File size: $(du -h dist/FabriCalc | cut -f1)"
        
        # Make executable
        chmod +x dist/FabriCalc
        print_status "Made executable file executable"
        
        print_status "Build process completed successfully!"
        print_status "You can now run: ./dist/FabriCalc"
        
    else
        print_error "Executable was not created in dist/FabriCalc"
        exit 1
    fi
    
else
    print_error "Build failed!"
    print_error "Check the error messages above for details"
    exit 1
fi 