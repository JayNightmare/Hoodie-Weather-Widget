<div align="center">

# 🧥 Hoodie Weather Widget
    
[![CI/CD Pipeline](https://github.com/JayNightmare/Hoodie-Weather-Widget/actions/workflows/ci.yml/badge.svg)](https://github.com/JayNightmare/Hoodie-Weather-Widget/actions/workflows/ci.yml)
[![Release](https://github.com/JayNightmare/Hoodie-Weather-Widget/actions/workflows/release.yml/badge.svg)](https://github.com/JayNightmare/Hoodie-Weather-Widget/actions/workflows/release.yml)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

</div>



A beautiful desktop weather widget that helps you decide if you need a hoodie! Perfect for those who want to stay comfortable in changing weather conditions.

![Hoodie Weather Widget](docs/widget-screenshot.png)

## ✨ Features

- 🌤️ **Real-time Weather Data**: Uses free Open-Meteo API
- 🧥 **Smart Hoodie Recommendations**: AI-powered comfort level calculation
- 📍 **Flexible Location**: Auto-detect or manual location setting
- 🎨 **Modern UI**: Beautiful, translucent widget design
- 📱 **Responsive**: Always-on-top, draggable widget
- ⚙️ **Configurable**: Easy settings panel
- 🔄 **Auto-updates**: Configurable refresh intervals
- 💻 **Cross-platform**: Works on Windows, macOS, and Linux

## 🚀 Easy Installation (Professional Windows Installer)

### 🌟 Recommended - Windows Installer (No Security Warnings!)
1. **Download** `HoodieWeatherSetup.exe` from [Releases](https://github.com/JayNightmare/Hoodie-Weather-Widget/releases)
2. **Double-click** the installer - trusted Windows installation wizard
3. **Follow the setup wizard** - automatic Python detection and guidance
4. **Choose your options** - shortcuts, auto-startup, etc.
5. **Launch and enjoy!** - professional Windows integration

### 🎯 Alternative - Portable Version
1. **Download** `HoodieWeatherWidget_Portable.zip`
2. **Extract** and double-click `HoodieWeather.exe`
3. **Done!** No installation required

### 🛠️ For Developers
```bash
git clone https://github.com/JayNightmare/Hoodie-Weather-Widget.git
cd Hoodie-Weather-Widget
pip install -r requirements.txt
python weather_widget_app.py
```

## 🔨 Building the Application

The project includes powerful build tools in the `start/` folder for creating distribution packages:

### Quick Build (Recommended)
```bash
# Windows - Creates both portable and installer packages
quick_build.bat

# Or run the Python script directly
cd start
python build_executable.py
```

### Custom Build Options
```bash
cd start

# Build only portable package
python build_executable.py --portable-only

# Build only Windows installer
python build_executable.py --installer-only

# Skip executable build (use existing)
python build_executable.py --no-build

# Build executable only (no packages)
python build_executable.py --no-build
# Then create packages separately
```

### Build Output Structure
All build artifacts are organized in the `output/` folder:
```
output/
├── build/                           # PyInstaller temporary files
├── dist/
│   └── HoodieWeather.exe           # Main executable
├── HoodieWeather.spec              # PyInstaller spec file
├── HoodieWeatherWidget_Portable/   # Portable package folder
│   ├── HoodieWeather.exe
│   └── README.txt
└── installer_output/
    └── HoodieWeatherSetup.exe      # Windows installer
```

### Build Requirements
- **Python 3.8+** with pip
- **PyInstaller** (auto-installed during build)
- **Inno Setup** (for Windows installer) - [Download here](https://jrsoftware.org/isinfo.php)

## 🏆 Why Use the Windows Installer?

✅ **Trusted by users** - Professional Windows installer experience  
✅ **No security warnings** - No `.bat` file trust issues  
✅ **Smart Python detection** - Guides users to install Python if needed  
✅ **Automatic shortcuts** - Desktop and Start Menu integration  
✅ **Clean uninstall** - Proper Windows Add/Remove Programs entry  
✅ **Optional auto-startup** - Starts with Windows if desired  
✅ **Modern wizard interface** - Familiar Windows installation process

## 📱 How to Use

### Starting the Widget
- **Portable**: Double-click `HoodieWeather.exe` 
- **Installed**: Use desktop shortcut "🧥 Hoodie Weather"
- Widget appears in top-right corner automatically

### Widget Controls
- **⚙️ Gear**: Settings and location configuration
- **❌ X**: Close widget
- **Drag**: Move widget anywhere on screen
- **Right-click**: View detailed location info

## ✨ User-Friendly Features

- 🎯 **Zero Configuration**: Works immediately out of the box
- 🌍 **Auto-Location**: Detects your location automatically  
- ⚡ **Quick Build**: `quick_build.bat` creates all distribution packages
- 🖥️ **Desktop Integration**: Shortcuts and startup options
- 🧥 **Smart Recommendations**: AI-powered hoodie comfort analysis

## 🎯 How It Works

The widget calculates hoodie comfort using multiple factors:

- 🌡️ **Temperature**: Core comfort calculation
- 💨 **Wind Speed**: Wind chill effect
- 💧 **Humidity**: Perceived temperature
- 🌧️ **Precipitation**: Weather protection needs

### Comfort Levels
- 🟢 **Green Zone**: Perfect hoodie weather (10-15°C)
- 🟡 **Yellow Zone**: Good for light hoodie (5-22°C)
- 🔴 **Red Zone**: Too warm for hoodie (>28°C)

## ⚙️ Configuration

Click the ⚙️ settings button to configure:

- 📍 **Location Mode**: Auto-detect or manual
- 🌍 **Custom Location**: Set any city worldwide
- 🔄 **Update Interval**: How often to refresh weather
- 🎨 **Theme Options**: UI customization

## 🏗️ Project Structure

```
Hoodie-Weather-Widget/
├── start/                          # 🔨 Build tools and scripts
│   └── build_executable.py        # Main build script with options
├── src/                            # 📦 Source code modules
│   ├── ui/                        # User interface components
│   ├── api/                       # Weather API and location services  
│   └── core/                      # Core business logic and settings
├── config/                         # ⚙️ Configuration files
├── docs/                          # 📚 Documentation
├── assets/                        # 🎨 Icons and images
├── output/                        # 📁 Build outputs (created during build)
├── weather_widget_app.py          # 🚀 Main application entry point
├── quick_build.bat                # ⚡ Quick build script for Windows
└── installer_script.iss           # 🔧 Inno Setup installer script
```

### Key Features
- **🆓 No API key required** - works out of the box!
- **🌍 Global coverage** - provides accurate weather data worldwide
- **🔒 Privacy-focused** - no data collection or tracking

## Widget Features
1. **Auto-start with Windows**: The setup script adds the widget to Windows startup
2. **Top-right positioning**: Widget appears in the top-right corner of your screen
3. **Weather data**: Shows temperature, humidity, wind speed, and precipitation
4. **Hoodie comfort indicator**: 3-part progress bar (Green = Perfect, Yellow = OK, Red = Too warm)
5. **Smart recommendations**: Considers temperature, wind, humidity, and precipitation

## Hoodie Comfort Algorithm
- **Perfect (Green)**: 10-22°C, low humidity, moderate wind
- **Good (Yellow)**: 22-28°C or high humidity conditions
- **Too Warm (Red)**: Above 28°C

## Project Structure
The widget is organized into a modular structure for easier maintenance and building:
- `start/` - Build tools and automation scripts
- `src/ui/` - User interface components
- `src/api/` - Weather API and location services  
- `src/core/` - Core business logic and settings
- `config/` - Configuration files
- `docs/` - Documentation
- `output/` - Generated build artifacts (created during build process)

## Customization
You can modify the following in `src/ui/weather_widget.py`:
- Window size and position
- Update frequency (default: 10 minutes)
- Temperature thresholds for hoodie recommendations
- Colors and styling in `src/ui/ui_components.py`

## Usage
- **Drag**: Click and drag to move the widget
- **Settings**: Click the ⚙ button to open location settings
- **Close**: Click the × button in the top-right corner
- **Location info**: Right-click for detailed location information
- **Auto-hide**: Widget stays on top but is semi-transparent

## Troubleshooting
- If weather data shows "Loading...", check your internet connection
- Widget automatically falls back to demo data if the API is unavailable
- For startup issues, check that Python is installed and in your PATH
