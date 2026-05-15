# Build script for Mo-Tech pubgm
# Creates a standalone executable using PyInstaller

import os
import sys
import subprocess

def build():
    print("Building Mo-Tech pubgm...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    build_command = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "Mo-Tech-pubgm",
        "--icon", "assets/icons/logo.ico",
        "--add-data", "assets;assets",
        "src/main.py"
    ]
    
    print("Running PyInstaller...")
    subprocess.check_call(build_command)
    
    print("\n✓ Build complete!")
    print("Executable location: dist/Mo-Tech-pubgm.exe")

if __name__ == "__main__":
    build()
