# Settings Demo Guide

## How to Use the New Settings Feature

### 1. Opening Settings
- Click the **⚙** (gear icon) button in the widget to open settings
- The settings window will appear near the widget

### 2. Location Options

#### Auto-detect Location (Default)
- Uses your IP address to determine location
- Automatically detects city, region, and country
- No configuration needed

#### Manual Location
- Allows you to set any location worldwide
- Enter in format: "City, Country" (e.g., "London, UK", "Tokyo, Japan")
- Click "Test Location" to verify before saving
- Shows exact coordinates and weather data

### 3. Settings Features

#### Location Testing
- **Test Location** button verifies your manual location
- Shows the full address, coordinates, and current temperature
- Helps ensure you're getting weather for the right place

#### Current Location Info
- Displays your current location and coordinates
- Shows whether using auto-detect or manual location
- Updates in real-time

#### Save & Apply
- **Save Settings** - Saves your preferences and immediately updates weather
- **Cancel** - Closes without saving changes
- **Reset to Auto** - Switches back to auto-detection

### 4. Visual Indicators

#### Location Icons
- 📍 = Auto-detected location
- 📌 = Manual location (with "Manual" text)

#### Right-click Info
- Right-click anywhere on the widget for detailed location popup
- Shows coordinates, mode (auto/manual), and full location name

### 5. Settings Persistence
- Settings are saved to `widget_settings.json`
- Automatically loads your preferences on widget restart
- Manual location survives computer restarts

## Example Usage

1. **Set London weather**: Enter "London, UK" in manual location
2. **Set specific area**: Enter "Manhattan, New York, USA" for precise location
3. **International**: Enter "Tokyo, Japan" or "Sydney, Australia"
4. **Reset**: Use "Reset to Auto" to go back to IP-based detection

## Benefits

- **Accuracy**: Set exact location instead of relying on IP detection
- **Privacy**: No need to share real location if using public/VPN IP
- **Travel**: Set home location when traveling
- **Specific areas**: Target specific districts within cities
