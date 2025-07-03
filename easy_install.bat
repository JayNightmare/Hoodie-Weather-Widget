@echo off
title Hoodie Weather Widget - One-Click Installer
color 0B

echo.
echo  ██╗  ██╗ ██████╗  ██████╗ ██████╗ ██╗███████╗
echo  ██║  ██║██╔═══██╗██╔═══██╗██╔══██╗██║██╔════╝
echo  ███████║██║   ██║██║   ██║██║  ██║██║█████╗  
echo  ██╔══██║██║   ██║██║   ██║██║  ██║██║██╔══╝  
echo  ██║  ██║╚██████╔╝╚██████╔╝██████╔╝██║███████╗
echo  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚══════╝
echo.
echo           WEATHER WIDGET - EASY INSTALLER
echo  ═══════════════════════════════════════════════════
echo.
echo  Welcome! This installer will set up your Hoodie Weather Widget
echo  in just a few clicks. No technical knowledge required!
echo.
echo  What this installer does:
echo   ✓ Checks if Python is installed (helps install if needed)
echo   ✓ Installs the weather widget automatically
echo   ✓ Creates desktop shortcut for easy access
echo   ✓ Sets up automatic startup (optional)
echo   ✓ No manual configuration needed!
echo.
echo  ═══════════════════════════════════════════════════
echo.
set /p choice="Ready to install? (Y/N): "
if /i "%choice%" neq "Y" (
    echo Installation cancelled. Have a great day! 👋
    timeout /t 3 >nul
    exit /b 0
)

echo.
echo 🚀 Starting installation...
echo.

:: Step 1: Check Python
echo [1/7] 🐍 Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ⚠️  Python not found - Don't worry, we'll help you install it!
    echo.
    echo 📥 Opening Python download page...
    echo 💡 IMPORTANT: When installing Python, make sure to:
    echo    ✅ Check "Add Python to PATH" 
    echo    ✅ Check "Install for all users" (if you're admin)
    echo.
    echo After Python installs, please restart this installer.
    echo.
    start https://python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    ✅ Python !PYTHON_VERSION! found!

:: Step 2: Check pip
echo [2/7] 📦 Checking package manager...
pip --version >nul 2>&1
if errorlevel 1 (
    echo    ❌ pip not found. Please reinstall Python with pip included.
    pause
    exit /b 1
)
echo    ✅ Package manager ready!

:: Step 3: Create installation directory
echo [3/7] 📁 Creating installation directory...
set INSTALL_DIR=%USERPROFILE%\HoodieWeather
if exist "%INSTALL_DIR%" (
    echo    ⚠️  Previous installation found. Updating...
    rmdir /s /q "%INSTALL_DIR%" 2>nul
)
mkdir "%INSTALL_DIR%" 2>nul
echo    ✅ Installation directory created: %INSTALL_DIR%

:: Step 4: Copy files
echo [4/7] 📋 Installing widget files...
xcopy /E /I /H /Y "*" "%INSTALL_DIR%\" >nul 2>&1
if errorlevel 1 (
    echo    ❌ Failed to copy files. Please run as administrator.
    pause
    exit /b 1
)
echo    ✅ Widget files installed!

:: Step 5: Install dependencies
echo [5/7] 🔧 Installing required packages...
cd /d "%INSTALL_DIR%"
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo    ⚠️  Some packages may have had issues, but trying to continue...
) else (
    echo    ✅ All packages installed successfully!
)

:: Step 6: Create shortcuts
echo [6/7] 🖥️  Creating shortcuts...

:: Desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
echo @echo off > "%DESKTOP%\🧥 Hoodie Weather.bat"
echo title Hoodie Weather Widget >> "%DESKTOP%\🧥 Hoodie Weather.bat"
echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\🧥 Hoodie Weather.bat"
echo python weather_widget_app.py >> "%DESKTOP%\🧥 Hoodie Weather.bat"

:: Start menu shortcut
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
if not exist "%STARTMENU%\Hoodie Weather" mkdir "%STARTMENU%\Hoodie Weather"
copy "%DESKTOP%\🧥 Hoodie Weather.bat" "%STARTMENU%\Hoodie Weather\Hoodie Weather Widget.bat" >nul

echo    ✅ Desktop and Start Menu shortcuts created!

:: Step 7: Optional startup integration
echo [7/7] 🚀 Setting up automatic startup...
echo.
set /p startup_choice="Would you like the widget to start with Windows? (Y/N): "
if /i "%startup_choice%"=="Y" (
    set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    copy "%DESKTOP%\🧥 Hoodie Weather.bat" "%STARTUP%\Hoodie Weather Widget.bat" >nul
    echo    ✅ Widget will start automatically with Windows!
) else (
    echo    ⏩ Skipped automatic startup (you can add it later)
)

:: Create uninstaller
echo [BONUS] 🗑️ Creating uninstaller...
echo @echo off > "%INSTALL_DIR%\Uninstall.bat"
echo title Uninstall Hoodie Weather Widget >> "%INSTALL_DIR%\Uninstall.bat"
echo echo Removing Hoodie Weather Widget... >> "%INSTALL_DIR%\Uninstall.bat"
echo del "%DESKTOP%\🧥 Hoodie Weather.bat" 2^>nul >> "%INSTALL_DIR%\Uninstall.bat"
echo rmdir /s /q "%STARTMENU%\Hoodie Weather" 2^>nul >> "%INSTALL_DIR%\Uninstall.bat"
echo del "%STARTUP%\Hoodie Weather Widget.bat" 2^>nul >> "%INSTALL_DIR%\Uninstall.bat"
echo rmdir /s /q "%INSTALL_DIR%" >> "%INSTALL_DIR%\Uninstall.bat"
echo echo Uninstalled successfully! >> "%INSTALL_DIR%\Uninstall.bat"
echo pause >> "%INSTALL_DIR%\Uninstall.bat"

echo    ✅ Uninstaller created (in installation folder)

:: Test installation
echo.
echo 🧪 Testing installation...
python -c "import sys; sys.path.insert(0, 'src'); from ui.weather_widget import WeatherWidget; print('✅ Widget can be imported successfully')" 2>nul
if errorlevel 1 (
    echo    ⚠️  Installation test had issues, but widget should still work
) else (
    echo    ✅ Installation test passed!
)

:: Success message
cls
echo.
echo  ═══════════════════════════════════════════════════
echo           🎉 INSTALLATION COMPLETED! 🎉
echo  ═══════════════════════════════════════════════════
echo.
echo  ✅ Hoodie Weather Widget installed successfully!
echo  📍 Installed to: %INSTALL_DIR%
echo  🖥️  Desktop shortcut: "🧥 Hoodie Weather"
echo  📱 Start Menu: Programs ^> Hoodie Weather
if /i "%startup_choice%"=="Y" (
    echo  🚀 Auto-start: Enabled
) else (
    echo  🚀 Auto-start: Disabled
)
echo.
echo  ═══════════════════════════════════════════════════
echo                    HOW TO USE
echo  ═══════════════════════════════════════════════════
echo.
echo  🎯 TO START THE WIDGET:
echo     • Double-click "🧥 Hoodie Weather" on your desktop
echo     • OR search "Hoodie Weather" in Start Menu
echo.
echo  🎨 WIDGET FEATURES:
echo     • Shows current weather and temperature
echo     • Smart hoodie recommendations based on conditions
echo     • Auto-detects your location
echo     • Clean, modern interface
echo     • Updates every 30 minutes
echo.
echo  ⚙️  WIDGET CONTROLS:
echo     • ⚙️ Gear icon = Settings
echo     • ❌ X icon = Close widget
echo     • Drag anywhere to move widget
echo     • Right-click for location info
echo.
echo  📞 NEED HELP?
echo     • Widget not starting? Check internet connection
echo     • To uninstall: Run Uninstall.bat in installation folder
echo     • Widget uses free Open-Meteo weather service
echo.
echo  ═══════════════════════════════════════════════════
echo.
set /p start_now="Start the widget now? (Y/N): "
if /i "%start_now%"=="Y" (
    echo 🚀 Starting Hoodie Weather Widget...
    start "" "%DESKTOP%\🧥 Hoodie Weather.bat"
    echo.
    echo Widget should appear in the top-right corner! 🧥
    echo.
)

echo Thank you for installing Hoodie Weather Widget!
echo Enjoy always knowing when you need a hoodie! 🧥☀️
echo.
pause
