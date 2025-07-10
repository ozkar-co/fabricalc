#!/bin/bash

# Build script for FabriCalc Linux executable

echo "Building FabriCalc for Linux..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Create the executable
pyinstaller --onefile \
            --windowed \
            --name FabriCalc \
            --add-data "config.json:." \
            --icon=icon.ico \
            main.py

echo "Build completed!"
echo "Executable location: dist/FabriCalc" 