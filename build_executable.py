#!/usr/bin/env python3
"""
Build script to create a standalone executable for Hoodie Weather Widget
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    print("🔨 Building Hoodie Weather Widget executable...")
    print("=" * 50)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        import PyInstaller
    
    # Clean previous builds
    if os.path.exists("build"):
        shutil.rmtree("build")
        print("🧹 Cleaned build directory")
    
    if os.path.exists("dist"):
        shutil.rmtree("dist")
        print("🧹 Cleaned dist directory")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name=HoodieWeather",         # Executable name
        "--add-data=src;src",           # Include source directory
        "--add-data=config;config",     # Include config directory if exists
        "--hidden-import=tkinter",      # Ensure tkinter is included
        "--hidden-import=requests",     # Ensure requests is included
        "--hidden-import=json",         # Ensure json is included
        "--clean",                      # Clean cache
        "weather_widget_app.py"         # Main script
    ]
    
    # Add icon if available
    if os.path.exists("icon.ico"):
        cmd.extend(["--icon=icon.ico"])
    
    print(f"🚀 Running: {' '.join(cmd)}")
    print()
    
    # Build the executable
    try:
        subprocess.check_call(cmd)
        print()
        print("✅ Build completed successfully!")
        
        # Check if executable was created
        exe_path = Path("dist/HoodieWeather.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            print()
            print("🎉 Ready for distribution!")
            print("Users can now just double-click HoodieWeather.exe to run the widget!")
        else:
            print("❌ Executable not found in dist/ directory")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        return False
    
    return True

def create_distribution_package():
    """Create a complete distribution package"""
    
    if not os.path.exists("dist/HoodieWeather.exe"):
        print("❌ Executable not found. Run build first.")
        return False
    
    print("📦 Creating distribution package...")
    
    # Create distribution folder
    dist_folder = "HoodieWeatherWidget_Portable"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    
    # Copy executable
    shutil.copy2("dist/HoodieWeather.exe", f"{dist_folder}/HoodieWeather.exe")
    
    # Create simple README for users
    readme_content = """# 🧥 Hoodie Weather Widget - Portable Version

## Quick Start
1. Double-click "HoodieWeather.exe" to start the widget
2. The widget will appear in the top-right corner of your screen
3. Click the ⚙ (gear) button to configure settings
4. Click the ❌ button to close the widget

## Features
- 🌡️ Real-time weather data
- 🧥 Smart hoodie recommendations
- 📍 Auto-location detection
- 🎨 Modern, translucent design
- 🔄 Automatic updates every 30 minutes

## No Installation Required!
This is a portable version - no installation needed.
Just run the .exe file and enjoy!

## Settings
- Right-click the widget for location info
- Use the gear button for full settings
- Widget remembers your preferences

## Troubleshooting
- If the widget doesn't start, ensure you have internet connection
- Windows Defender might scan the file first time (this is normal)
- Widget requires Windows 10 or later

Made with ❤️ for hoodie lovers everywhere!
"""
    
    with open(f"{dist_folder}/README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print(f"✅ Distribution package created: {dist_folder}/")
    print("📋 Package contents:")
    print("   - HoodieWeather.exe (main application)")
    print("   - README.txt (user instructions)")
    
    return True

if __name__ == "__main__":
    print("🧥 Hoodie Weather Widget - Build Tool")
    print("=" * 40)
    print()
    
    if build_executable():
        print()
        create_distribution_package()
        print()
        print("🎉 Build process complete!")
        print("📦 Share the 'HoodieWeatherWidget_Portable' folder with users")
        print("👥 Users just need to double-click HoodieWeather.exe to run!")
    else:
        print("❌ Build failed. Please check errors above.")
        sys.exit(1)
