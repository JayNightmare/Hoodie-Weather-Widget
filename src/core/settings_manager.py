"""
Settings manager module for storing and retrieving widget settings.
"""

import json
import os


class SettingsManager:
    """Handle widget settings persistence"""

    def __init__(self, settings_file="../config/widget_settings.json"):
        # Use config directory relative to core module
        current_dir = os.path.dirname(__file__)
        config_dir = os.path.join(os.path.dirname(current_dir), "config")
        os.makedirs(config_dir, exist_ok=True)

        if not os.path.isabs(settings_file):
            self.settings_file = os.path.join(
                config_dir, os.path.basename(settings_file)
            )
        else:
            self.settings_file = settings_file

        self.default_settings = {
            "manual_location": None,
            "update_interval": 600,  # 10 minutes
            "window_position": None,
            "transparency": 0.95,
            "theme": "dark",
        }

    def load_settings(self):
        """Load settings from file, return defaults if file doesn't exist"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                    # Merge with defaults to handle missing keys
                    merged_settings = self.default_settings.copy()
                    merged_settings.update(settings)
                    print(f"Loaded settings: {merged_settings}")
                    return merged_settings
            else:
                print("Settings file not found, using defaults")
                return self.default_settings.copy()
        except Exception as e:
            print(f"Error loading settings: {e}")
            return self.default_settings.copy()

    def save_settings(self, settings):
        """Save settings to file"""
        try:
            with open(self.settings_file, "w") as f:
                json.dump(settings, f, indent=2)
            print(f"Settings saved: {settings}")
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False

    def get_setting(self, key, default=None):
        """Get a specific setting value"""
        settings = self.load_settings()
        return settings.get(key, default)

    def update_setting(self, key, value):
        """Update a specific setting"""
        settings = self.load_settings()
        settings[key] = value
        return self.save_settings(settings)

    def reset_settings(self):
        """Reset all settings to defaults"""
        return self.save_settings(self.default_settings.copy())
