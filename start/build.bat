@echo off
title Hoodie Weather Widget - Build System
color 0A

echo.
echo ================================================================
echo 🧥 Hoodie Weather Widget - Build System
echo ================================================================
echo.

:MENU
echo Select build option:
echo.
echo [1] Build Everything (Portable + Installer)
echo [2] Build Portable Version Only
echo [3] Build Windows Installer Only
echo [4] Build Executable Only
echo [5] Create Installer from Existing Executable
echo [6] Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto BUILD_ALL
if "%choice%"=="2" goto BUILD_PORTABLE
if "%choice%"=="3" goto BUILD_INSTALLER
if "%choice%"=="4" goto BUILD_EXE
if "%choice%"=="5" goto BUILD_INSTALLER_ONLY
if "%choice%"=="6" goto EXIT

echo Invalid choice. Please try again.
echo.
goto MENU

:BUILD_ALL
echo.
echo 🎁 Building complete release package...
python build_executable.py
goto DONE

:BUILD_PORTABLE
echo.
echo 📦 Building portable version only...
python build_executable.py --portable-only
goto DONE

:BUILD_INSTALLER
echo.
echo 🔧 Building Windows installer only...
python build_executable.py --installer-only
goto DONE

:BUILD_EXE
echo.
echo ⚙️ Building executable only...
python build_executable.py --no-build=false
if not exist "../output/dist\HoodieWeather.exe" (
    echo ❌ Build failed!
    pause
    goto MENU
)
echo ✅ Executable built successfully!
goto DONE

:BUILD_INSTALLER_ONLY
echo.
echo 🔧 Creating installer from existing executable...
if not exist "../output/dist\HoodieWeather.exe" (
    echo ❌ No executable found! Build the executable first.
    pause
    goto MENU
)
python build_executable.py --installer-only --no-build
goto DONE

:DONE
echo.
echo ================================================================
echo 🎉 Build Complete!
echo ================================================================
echo.

if exist "../output/HoodieWeatherWidget_Portable" (
    echo ✅ Portable Package: HoodieWeatherWidget_Portable\
)

if exist "../output/installer_output\HoodieWeatherSetup.exe" (
    echo ✅ Windows Installer: installer_output\HoodieWeatherSetup.exe
)

echo.
echo 💡 Distribution Tips:
echo    - Use the installer for most users (easier, no security warnings)
echo    - Use portable for users who prefer no installation
echo    - Both versions are fully functional
echo.

:ASK_CONTINUE
set /p continue="Build another version? (y/n): "
if /i "%continue%"=="y" goto MENU
if /i "%continue%"=="yes" goto MENU

:EXIT
echo.
echo 👋 Thanks for using Hoodie Weather Widget Build System!
pause
