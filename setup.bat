@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo   Hoodie Weather Widget Setup
echo ========================================
echo.

:: Check if Python is installed and get version
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8 or higher from:
    echo https://python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Get and display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python !PYTHON_VERSION! found

:: Check Python version (basic check for 3.x)
echo [2/6] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>nul
if errorlevel 1 (
    echo ❌ ERROR: Python 3.8 or higher is required.
    echo Current version: !PYTHON_VERSION!
    pause
    exit /b 1
)
echo ✅ Python version is compatible

:: Check if pip is available
echo [3/6] Checking pip availability...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip is not available.
    echo Please reinstall Python with pip included.
    pause
    exit /b 1
)
echo ✅ pip is available

:: Check if requirements.txt exists
echo [4/6] Checking project files...
if not exist "requirements.txt" (
    echo ❌ ERROR: requirements.txt not found.
    echo Please ensure you're running this script from the project directory.
    pause
    exit /b 1
)

if not exist "weather_widget_app.py" (
    echo ❌ ERROR: weather_widget_app.py not found.
    echo Please ensure you're running this script from the project directory.
    pause
    exit /b 1
)

if not exist "start_widget.bat" (
    echo ❌ ERROR: start_widget.bat not found.
    echo Please ensure you're running this script from the project directory.
    pause
    exit /b 1
)
echo ✅ All required files found

:: Install requirements
echo [5/6] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ ERROR: Failed to install dependencies.
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

:: Setup startup integration
echo [6/6] Setting up Windows startup integration...
set startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

:: Create startup folder if it doesn't exist
if not exist "%startup_folder%" (
    mkdir "%startup_folder%"
)

:: Copy the startup script to startup folder
copy "start_widget.bat" "%startup_folder%\Hoodie Weather Widget.bat" >nul
if errorlevel 1 (
    echo ⚠️  Warning: Could not add to startup folder.
    echo You may need to run this script as administrator.
    echo You can manually copy start_widget.bat to startup if needed.
) else (
    echo ✅ Added to Windows startup
)

:: Create config directory if it doesn't exist
if not exist "config" mkdir config

echo.
echo ========================================
echo           Setup Complete! 🎉
echo ========================================
echo.
echo ✅ Python environment verified
echo ✅ Dependencies installed
echo ✅ Widget added to Windows startup
echo.
echo The widget will start automatically when Windows boots.
echo You can also run it manually by double-clicking:
echo   - start_widget.bat (for normal use)
echo   - weather_widget_app.py (for development)
echo.
echo 📡 Uses free Open-Meteo API (no API key required)
echo 🌍 Auto-detects your location
echo 🧥 Provides hoodie comfort recommendations
echo.
echo Press any key to exit...
pause >nul