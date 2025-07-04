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

    # Ensure output directory exists
    os.makedirs("../output", exist_ok=True)

    # Clean previous builds
    if os.path.exists("../output/build"):
        shutil.rmtree("../output/build")
        print("🧹 Cleaned build directory")

    if os.path.exists("../output/dist"):
        shutil.rmtree("../output/dist")
        print("🧹 Cleaned dist directory")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable file
        "--windowed",  # No console window
        "--name=HoodieWeather",  # Executable name
        "--distpath=../output/dist",  # Output executable to output/dist
        "--workpath=../output/build",  # Use output/build for work files
        "--specpath=../output",  # Put .spec file in output folder
        f"--add-data={os.path.abspath('../src')};src",  # Include source directory with absolute path
        # "--add-data=config;config",     # Include config directory if exists
        "--hidden-import=tkinter",  # Ensure tkinter is included
        "--hidden-import=requests",  # Ensure requests is included
        "--hidden-import=json",  # Ensure json is included
        "--clean",  # Clean cache
        "../weather_widget_app.py",  # Main script
    ]

    # Add icon if available
    if os.path.exists("../assets/icon.ico"):
        cmd.extend(["--icon=../assets/icon.ico"])

    print(f"🚀 Running: {' '.join(cmd)}")
    print()

    # Build the executable
    try:
        subprocess.check_call(cmd)
        print()
        print("✅ Build completed successfully!")

        # Check if executable was created
        exe_path = Path("../output/dist/HoodieWeather.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 Executable created: {exe_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            print()
            print("🎉 Ready for distribution!")
            print(
                "Users can now just double-click HoodieWeather.exe to run the widget!"
            )
        else:
            print("❌ Executable not found in dist/ directory")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error: {e}")
        return False

    return True


def create_distribution_package():
    """Create a complete distribution package"""

    if not os.path.exists("../output/dist/HoodieWeather.exe"):
        print("❌ Executable not found. Run build first.")
        return False

    print("📦 Creating distribution package...")

    # Create distribution folder
    dist_folder = "../output/HoodieWeatherWidget_Portable"
    if os.path.exists(dist_folder):
        shutil.rmtree(dist_folder)

    os.makedirs(dist_folder)

    # Copy executable
    shutil.copy2("../output/dist/HoodieWeather.exe", f"{dist_folder}/HoodieWeather.exe")

    # Copy config if it exists
    if os.path.exists("../src/config"):
        shutil.copytree("config", f"{dist_folder}/config")

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
    if os.path.exists("../src/config"):
        print("   - config/ (default settings)")

    return True


def create_installer():
    """Create Windows installer using Inno Setup"""

    if not os.path.exists("../output/dist/HoodieWeather.exe"):
        print("❌ Executable not found. Run build first.")
        return False

    print("🔧 Creating Windows Installer...")
    print("=" * 40)

    # Check if Inno Setup is installed
    # Search all drives for Inno Setup paths
    inno_paths = []
    for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive_path = f"{drive}:\\"
        if os.path.exists(drive_path):
            inno_paths.extend(
                [
                    os.path.join(
                        drive_path, "Program Files (x86)", "Inno Setup 6", "ISCC.exe"
                    ),
                    os.path.join(
                        drive_path, "Program Files", "Inno Setup 6", "ISCC.exe"
                    ),
                    os.path.join(
                        drive_path, "Program Files (x86)", "Inno Setup 5", "ISCC.exe"
                    ),
                    os.path.join(
                        drive_path, "Program Files", "Inno Setup 5", "ISCC.exe"
                    ),
                ]
            )

    inno_compiler = None
    for path in inno_paths:
        if os.path.exists(path):
            inno_compiler = path
            break

    if not inno_compiler:
        print("❌ Inno Setup not found!")
        print("📥 Please install Inno Setup from: https://jrsoftware.org/isinfo.php")
        print("💡 After installation, run this script again to create the installer.")
        return False

    print(f"✅ Found Inno Setup: {inno_compiler}")

    # Create installer output directory
    if not os.path.exists("../output/installer_output"):
        os.makedirs("../output/installer_output")

    # Compile the installer
    script_path = "installer_script.iss"
    if not os.path.exists(script_path):
        print(f"❌ Installer script not found: {script_path}")
        return False

    print(f"🚀 Compiling installer script: {script_path}")

    try:
        cmd = [inno_compiler, script_path]
        subprocess.check_call(cmd)

        # Check if installer was created
        installer_path = "../output/installer_output/HoodieWeatherSetup.exe"
        if os.path.exists(installer_path):
            size_mb = os.path.getsize(installer_path) / (1024 * 1024)
            print()
            print("✅ Windows Installer created successfully!")
            print(f"📦 Installer: {installer_path}")
            print(f"📏 Size: {size_mb:.1f} MB")
            print()
            print("🎉 Professional installer ready!")
            print(
                "👥 Users can now run HoodieWeatherSetup.exe for guided installation!"
            )
            print("🔒 No security warnings - proper Windows installer format")
            return True
        else:
            print("❌ Installer file not found after compilation")
            return False

    except subprocess.CalledProcessError as e:
        print(f"❌ Installer compilation failed: {e}")
        print("💡 Check the installer script for syntax errors")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def build_release_packages():
    """Build both portable and installer packages"""

    print("🎁 Building Complete Release Packages")
    print("=" * 50)

    success_count = 0

    # Build portable version
    print("\n1️⃣ Creating Portable Package...")
    if create_distribution_package():
        success_count += 1
        print("✅ Portable package ready!")
    else:
        print("❌ Portable package failed!")

    # Build installer version
    print("\n2️⃣ Creating Windows Installer...")
    if create_installer():
        success_count += 1
        print("✅ Windows installer ready!")
    else:
        print("❌ Windows installer failed!")

    print(f"\n📊 Release Summary: {success_count}/2 packages created successfully")

    if success_count > 0:
        print("\n🎉 Release packages available:")
        if os.path.exists("../output/HoodieWeatherWidget_Portable"):
            print("   📁 ../output/HoodieWeatherWidget_Portable/ (portable version)")
        if os.path.exists("../output/installer_output/HoodieWeatherSetup.exe"):
            print(
                "   💾 ../output/installer_output/HoodieWeatherSetup.exe (Windows installer)"
            )

        print("\n💡 Distribution recommendations:")
        print("   🥇 Primary: HoodieWeatherSetup.exe (professional installer)")
        print("   🥈 Alternative: Portable folder (no installation needed)")

    return success_count == 2


if __name__ == "__main__":
    print("🧥 Hoodie Weather Widget - Build Tool")
    print("=" * 40)
    print()

    # Parse command line arguments
    import argparse

    parser = argparse.ArgumentParser(description="Build Hoodie Weather Widget")
    parser.add_argument(
        "--portable-only", action="store_true", help="Create only portable package"
    )
    parser.add_argument(
        "--installer-only", action="store_true", help="Create only Windows installer"
    )
    parser.add_argument(
        "--no-build", action="store_true", help="Skip executable build (use existing)"
    )

    args = parser.parse_args()

    # Build executable unless skipped
    build_success = True
    if not args.no_build:
        if not build_executable():
            print("❌ Build failed. Please check errors above.")
            sys.exit(1)
        print()
    else:
        print("⏭️ Skipping executable build (using existing)")
        if not os.path.exists("../output/dist/HoodieWeather.exe"):
            print("❌ No existing executable found. Run without --no-build first.")
            sys.exit(1)
        print()

    # Determine what packages to create
    if args.portable_only:
        print("📦 Creating portable package only...")
        success = create_distribution_package()
    elif args.installer_only:
        print("🔧 Creating installer only...")
        success = create_installer()
    else:
        print("� Creating both portable and installer packages...")
        success = build_release_packages()

    if success:
        print()
        print("�🎉 Build process complete!")
        if not args.installer_only:
            print("📦 Portable: Share the 'HoodieWeatherWidget_Portable' folder")
        if not args.portable_only:
            print("� Installer: Share 'installer_output/HoodieWeatherSetup.exe'")
        print("👥 Ready for distribution!")
    else:
        print("❌ Package creation failed. Please check errors above.")
        sys.exit(1)
