@echo off
REM Hoodie Weather Widget Startup Script
REM This script starts the weather widget application with proper error handling

REM Get the directory where this script is located
cd /d "%~dp0"

REM Set a flag file to prevent rapid restart loops
set "LOCKFILE=%TEMP%\hoodie_widget.lock"

REM Check if another instance is already running
if exist "%LOCKFILE%" (
    echo [INFO] Widget is already running or recently failed. Exiting to prevent loop.
    exit /b 0
)

REM Create lock file
echo %DATE% %TIME% > "%LOCKFILE%"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo.
    echo This error prevents the Hoodie Weather Widget from starting.
    echo Removing from startup to prevent repeated failures...
    del "%LOCKFILE%" >nul 2>&1
    REM Try to remove from startup folder to prevent restart loops
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Hoodie Weather Widget.bat" >nul 2>&1
    exit /b 1
)

REM Check if the main application file exists
if not exist "weather_widget_app.py" (
    echo [ERROR] weather_widget_app.py not found
    echo Make sure this script is in the same folder as the widget application
    echo.
    echo This error prevents the Hoodie Weather Widget from starting.
    echo Removing from startup to prevent repeated failures...
    del "%LOCKFILE%" >nul 2>&1
    REM Try to remove from startup folder to prevent restart loops
    del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Hoodie Weather Widget.bat" >nul 2>&1
    exit /b 1
)

REM Start the weather widget application
echo Starting Hoodie Weather Widget...
python weather_widget_app.py

REM Clean up lock file when done
del "%LOCKFILE%" >nul 2>&1

REM If we get here, the application has closed normally
echo Widget application closed.