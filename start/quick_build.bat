@echo off
title Quick Build - Hoodie Weather Widget
color 0E

echo.
echo ================================================================
echo 🧥 QUICK BUILD - Hoodie Weather Widget
echo ================================================================
echo.
echo This will build EVERYTHING automatically:
echo   1. Python executable (HoodieWeather.exe)
echo   2. Portable package (folder)
echo   3. Windows installer (HoodieWeatherSetup.exe)
echo.
echo Requirements:
echo   - Python 3.8+ installed
echo   - Inno Setup installed (for installer creation)
echo.

pause

echo.
echo 🔨 Starting automated build process...
echo ================================================================
echo.

python build_executable.py

echo.
echo ================================================================
echo ✅ Build process complete!
echo ================================================================
echo.

if exist "..\HoodieWeatherWidget_Portable" (
    echo ✅ Portable version: HoodieWeatherWidget_Portable\
)

if exist "..\installer_output\HoodieWeatherSetup.exe" (
    echo ✅ Windows installer: installer_output\HoodieWeatherSetup.exe
)

if exist "..\dist\HoodieWeather.exe" (
    echo ✅ Executable: dist\HoodieWeather.exe
)

echo.
echo 💡 To distribute:
echo    - Use HoodieWeatherSetup.exe for most users
echo    - Use portable folder for advanced users
echo.

pause
