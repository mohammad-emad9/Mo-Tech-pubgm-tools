"""
Mo-Tech pubgm - Setup Script
Developed by: Mohammed Emad
"""

import os
import sys
import shutil
from pathlib import Path

def create_directories():
    """Create necessary directories for the application"""
    dirs = [
        "assets/configs",
        "assets/logs",
        "src",
        "temp"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✓ Created directory: {dir_path}")

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✓ Python version: {sys.version}")
    return True

def check_tkinter():
    """Check if tkinter is available"""
    try:
        import tkinter as tk
        print("✓ Tkinter is available")
        return True
    except ImportError:
        print("❌ Error: Tkinter is not installed.")
        print("   Please install python3-tk package.")
        return False

def copy_icon():
    """Copy icon file to appropriate locations if needed"""
    icon_src = "assets/icons/logo.ico"
    if os.path.exists(icon_src):
        print(f"✓ Icon file found: {icon_src}")
        return True
    else:
        print("⚠ Warning: Icon file not found")
        return False

def create_default_config():
    """Create default configuration file"""
    config_path = "assets/configs/settings.json"
    default_config = {
        "fps_limit": 60,
        "graphics_quality": "Smooth",
        "visual_style": "Classic",
        "rendering_mode": "DirectX+",
        "shader_cache": True,
        "global_render_cache": True,
        "hardware_priority": "High",
        "ipad_view": False,
        "resolution": "1920x1080"
    }
    
    import json
    with open(config_path, 'w') as f:
        json.dump(default_config, f, indent=4)
    
    print(f"✓ Created default configuration: {config_path}")

def main():
    print("=" * 60)
    print("Mo-Tech pubgm - Setup Wizard")
    print("=" * 60)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check tkinter
    if not check_tkinter():
        sys.exit(1)
    
    # Create directories
    print("\nCreating directories...")
    create_directories()
    
    # Copy icon
    print("\nChecking assets...")
    copy_icon()
    
    # Create default config
    print("\nCreating default configuration...")
    create_default_config()
    
    print("\n" + "=" * 60)
    print("✓ Setup Complete!")
    print("=" * 60)
    print("\nTo run the application:")
    print("  python src/main.py")
    print("\nNote: Run as Administrator for full functionality on Windows")
    print()

if __name__ == "__main__":
    main()
