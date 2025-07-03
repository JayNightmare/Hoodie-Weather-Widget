@echo off
title Building Hoodie Weather Widget
echo.
echo 🔨 Building Hoodie Weather Widget for Distribution
echo ================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python first.
    pause
    exit /b 1
)

:: Install PyInstaller if not available
echo 📦 Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 📥 Installing PyInstaller...
    pip install pyinstaller
)

:: Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "HoodieWeatherWidget_Portable" rmdir /s /q "HoodieWeatherWidget_Portable"

echo 🚀 Building executable...
echo.

:: Build the executable
pyinstaller --onefile --windowed --name=HoodieWeather --add-data=src;src --add-data=config;config --hidden-import=tkinter --hidden-import=requests --clean weather_widget_app.py

if errorlevel 1 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

:: Check if executable was created
if not exist "dist\HoodieWeather.exe" (
    echo ❌ Executable not found!
    pause
    exit /b 1
)

echo ✅ Executable built successfully!

:: Create portable distribution
echo 📦 Creating portable distribution...
mkdir "HoodieWeatherWidget_Portable"
copy "dist\HoodieWeather.exe" "HoodieWeatherWidget_Portable\"
copy "easy_install.bat" "HoodieWeatherWidget_Portable\Install_Full_Version.bat"

:: Create portable README
echo # 🧥 Hoodie Weather Widget - Portable Version > "HoodieWeatherWidget_Portable\README.txt"
echo. >> "HoodieWeatherWidget_Portable\README.txt"
echo ## Quick Start >> "HoodieWeatherWidget_Portable\README.txt"
echo 1. Double-click "HoodieWeather.exe" to start >> "HoodieWeatherWidget_Portable\README.txt"
echo 2. Widget appears in top-right corner >> "HoodieWeatherWidget_Portable\README.txt"
echo 3. Click gear icon for settings >> "HoodieWeatherWidget_Portable\README.txt"
echo. >> "HoodieWeatherWidget_Portable\README.txt"
echo ## Features >> "HoodieWeatherWidget_Portable\README.txt"
echo - Real-time weather data >> "HoodieWeatherWidget_Portable\README.txt"
echo - Smart hoodie recommendations >> "HoodieWeatherWidget_Portable\README.txt"
echo - Auto-location detection >> "HoodieWeatherWidget_Portable\README.txt"
echo - No installation required! >> "HoodieWeatherWidget_Portable\README.txt"
echo. >> "HoodieWeatherWidget_Portable\README.txt"
echo Made with ❤️ for hoodie lovers! >> "HoodieWeatherWidget_Portable\README.txt"

echo.
echo ✅ Distribution package created!
echo.
echo 📁 Files created:
echo    • HoodieWeatherWidget_Portable\HoodieWeather.exe (portable version)
echo    • HoodieWeatherWidget_Portable\Install_Full_Version.bat (full installer)
echo    • HoodieWeatherWidget_Portable\README.txt (user instructions)
echo.
echo 🎉 Ready for distribution!
echo.
echo 👥 Users can now:
echo    • Just run HoodieWeather.exe (no installation)
echo    • Or run Install_Full_Version.bat (full installation with shortcuts)
echo.
pause
