# 🧥 Hoodie Weather Widget - User Guide

## 🚀 Three Ways to Install

### Option 1: Super Easy (Recommended for most users)
1. **Download** the `HoodieWeatherWidget_Portable` folder
2. **Double-click** `HoodieWeather.exe`
3. **That's it!** No installation required

### Option 2: Full Installation (With shortcuts and auto-start)
1. **Download** the project folder
2. **Double-click** `easy_install.bat`
3. **Follow** the prompts (it handles everything automatically)
4. **Enjoy** desktop shortcuts and auto-startup

### Option 3: Developer/Manual
1. **Download** the project folder
2. **Double-click** `setup.bat`
3. **Run** `start_widget.bat` to start

## 🎯 How to Use

### Starting the Widget
- **Portable**: Double-click `HoodieWeather.exe`
- **Installed**: Double-click desktop shortcut "🧥 Hoodie Weather"
- **Manual**: Run `start_widget.bat`

### Widget Controls
- **⚙️ Gear Icon**: Opens settings panel
- **❌ X Icon**: Closes the widget
- **Drag**: Click and drag anywhere to move the widget
- **Right-click**: Shows detailed location information

### Widget Display
```
┌─────────────────────────┐
│ 🧥 Hoodie Weather    ⚙❌│
│                         │
│    Kingston upon Thames │
│         23.0°C          │
│    Partly Cloudy        │
│  Humidity: 28% | Wind..│
│                         │
│   Hoodie Comfort Level  │
│ ████████████▒▒▒▒▒▒▒▒▒▒ │
│                         │
│ Great for a hoodie! 😊  │
│                         │
│   Last updated: 14:30   │
└─────────────────────────┘
```

## ⚙️ Settings Panel

Click the gear icon (⚙️) to access:

### Location Settings
- **🌐 Auto-detect location**: Uses your IP address
- **📌 Set location manually**: Enter any city/address
- **🌍 Test Location**: Verify your location works

### Current Information
- See your detected location
- View coordinates
- Check connection status

## 🎨 Widget Features

### Smart Recommendations
The widget considers:
- 🌡️ **Temperature**: Main comfort factor
- 💨 **Wind Speed**: Makes you feel cooler
- 💧 **Humidity**: Affects perceived temperature
- 🌧️ **Precipitation**: Weather protection needs

### Comfort Levels
- 🟢 **Green**: Perfect hoodie weather (10-15°C)
- 🟡 **Yellow**: Good for light hoodie (5-22°C)
- 🔴 **Red**: Too warm for hoodie (>28°C)

### Auto-Updates
- Refreshes every 30 minutes
- Shows "Last updated" timestamp
- Automatically retries if connection fails

## 🔧 Troubleshooting

### Widget Won't Start
1. **Check Internet**: Widget needs internet for weather data
2. **Windows Defender**: May scan .exe files first time (normal)
3. **Python Issues**: Use `easy_install.bat` to fix dependencies
4. **Blocked Popup**: Check if antivirus blocked the widget

### Location Issues
1. **Wrong Location**: Use manual location setting
2. **No Location Found**: Check internet connection
3. **Location Timeout**: Try again in a few minutes

### Performance Issues
1. **Widget Slow**: Check internet speed
2. **High CPU**: Restart the widget
3. **Memory Usage**: Close and restart if needed

### Common Error Messages

| Error | Solution |
|-------|----------|
| "Python not found" | Install Python or use portable version |
| "No internet connection" | Check your network connection |
| "Location detection failed" | Switch to manual location mode |
| "Weather API error" | Wait a moment and try again |

## 🗑️ Uninstalling

### Portable Version
- Simply delete the `HoodieWeather.exe` file

### Full Installation
- Run `Uninstall.bat` in the installation folder
- Or manually delete shortcuts and installation folder

## 🆘 Need Help?

### Quick Fixes
1. **Restart the widget**: Close and start again
2. **Check internet**: Make sure you're connected
3. **Reinstall**: Run `easy_install.bat` again
4. **Use portable**: Try the .exe version instead

### Widget Not Visible?
- Check top-right corner of screen
- Try moving windows around
- Widget might be behind other windows
- Restart widget to reset position

### Settings Not Saving?
- Make sure widget has write permissions
- Try running as administrator
- Check if antivirus is blocking file writes

## 💡 Tips & Tricks

### Best Practices
- 📍 **Set manual location** for more accurate weather
- 🔄 **Let it run in background** for continuous updates
- 📱 **Add to startup** for convenience
- 🎨 **Move widget** to preferred screen position

### Advanced Usage
- 🖱️ **Right-click** for detailed location info
- ⌨️ **Alt+Tab** to focus on widget
- 📋 **Multiple locations**: Restart widget and change location

### Performance Tips
- 💻 **Low-end PCs**: Use portable version
- 🔋 **Laptop Battery**: Widget uses minimal power
- 🌐 **Slow Internet**: Increase update interval in future versions

## 📊 Technical Details

### System Requirements
- **OS**: Windows 10/11 (7/8 may work)
- **RAM**: 50MB minimum
- **Storage**: 100MB for full installation
- **Internet**: Required for weather data

### Data Usage
- **Very Low**: ~1KB per weather update
- **Frequency**: Every 30 minutes
- **Provider**: Open-Meteo (free service)
- **Privacy**: No personal data stored

Made with ❤️ for hoodie enthusiasts everywhere! 🧥
