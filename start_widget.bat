@echo off
title 🧥 Hoodie Weather Widget
cd /d "%~dp0"

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo.
    echo 📥 Please install Python from: https://python.org/downloads/
    echo 💡 Make sure to check "Add Python to PATH" during installation
    echo.
    echo 🚀 Or use the easy installer: run easy_install.bat
    echo.
    pause
    exit /b 1
)

:: Show startup message
echo 🧥 Starting Hoodie Weather Widget...
echo 📍 Widget will appear in the top-right corner
echo ⚙️  Click the gear icon for settings
echo ❌ Click the X to close
echo.

:: Start the widget
python weather_widget_app.py

:: If the script ends unexpectedly, show error
if errorlevel 1 (
    echo.
    echo ❌ Widget stopped unexpectedly
    echo 📞 Try the following:
    echo    • Check your internet connection
    echo    • Run easy_install.bat to reinstall
    echo    • Make sure Python and dependencies are installed
    echo.
    pause
)
