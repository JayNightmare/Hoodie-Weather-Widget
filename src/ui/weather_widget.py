import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
import os
import sys

# Import from other modules in the project
from api.weather_api import WeatherAPI
from core.settings_manager import SettingsManager
from ui.ui_components import UIComponents
from core.hoodie_calculator import HoodieComfortCalculator

class WeatherWidget:
    def __init__(self):
        print("Initializing WeatherWidget...")
        self.root = tk.Tk()
        print("Tkinter root created...")
        self.setup_window()
        print("Window setup complete...")
        self.weather_data = {}
        self.city = "auto"  # Will auto-detect location
        self.manual_location = None  # For manually set location
        
        # Initialize modules
        self.weather_api = WeatherAPI()
        self.settings_manager = SettingsManager()
        self.hoodie_calculator = HoodieComfortCalculator()
        self.ui = UIComponents()
        
        print("Loading settings...")
        self.load_settings()
        print("Creating widgets...")
        self.create_widgets()
        print("Starting weather updates...")
        self.start_weather_updates()
        print("Widget initialization complete!")
        
    def setup_window(self):
        # Configure the main window using UIComponents with increased height
        UIComponents.setup_window_style(self.root, title="Hoodie Weather Widget", size="800x600",
                          topmost=True, alpha=0.95)
        
        # Position window at top-right of screen using the size parameter
        width, height = map(int, "300x360".split('x'))
        screen_width = self.root.winfo_screenwidth()
        x = screen_width - width - 20  # Width + 20 margin
        y = 20  # 20 pixels from top
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Remove title bar for widget-like appearance
        self.root.overrideredirect(True)
        
        # Bind events for window dragging
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.do_drag)
        self.root.bind('<Button-3>', self.show_location_info)  # Right-click for location info
        
    def start_drag(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def do_drag(self, event):
        x = self.root.winfo_x() + event.x - self.start_x
        y = self.root.winfo_y() + event.y - self.start_y
        self.root.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        # Create main frame using UIComponents
        main_frame = UIComponents.create_styled_frame(self.root, padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Add a top spacer frame for button positioning
        top_spacer = UIComponents.create_styled_frame(main_frame)
        top_spacer.pack(fill='x', pady=(0, 10))
        top_spacer.configure(height=25)
        
        # Settings button (small gear icon next to close button) - positioned in top spacer
        settings_btn = UIComponents.create_styled_button(
            top_spacer, text="⚙", command=self.open_settings,
            color='accent_blue', font='tiny', width=2, height=1
        )
        settings_btn.place(relx=0.7, rely=0.5, anchor='center')
        
        # Close button (small X in top-right) - positioned in top spacer
        close_btn = UIComponents.create_styled_button(
            top_spacer, text="✖", command=self.root.quit,
            color='accent_red', font='tiny', width=2, height=1
        )
        close_btn.place(relx=1.0, rely=0.5, anchor='e')
        
        # Title
        title_label = UIComponents.create_styled_label(
            main_frame, text="Hoodie Weather", font='title'
        )
        title_label.pack(pady=(0, 10))
        
        # Weather info frame
        weather_frame = UIComponents.create_styled_frame(main_frame)
        weather_frame.pack(fill='x', pady=(0, 10))
        
        # Location
        self.location_label = UIComponents.create_styled_label(
            weather_frame, text="Detecting location...", 
            font='small', color='text_secondary', wraplength=250
        )
        self.location_label.pack()
        
        # Temperature
        self.temp_label = UIComponents.create_styled_label(
            weather_frame, text="--°C", font='large', color='accent_blue'
        )
        self.temp_label.pack()
        
        # Weather details
        self.details_label = UIComponents.create_styled_label(
            weather_frame, text="Loading weather...", font='tiny'
        )
        self.details_label.pack()
        
        # Hoodie recommendation progress bar
        progress_frame = UIComponents.create_styled_frame(main_frame)
        progress_frame.pack(fill='x', pady=(0, 10))
        
        UIComponents.create_styled_label(
            progress_frame, text="Hoodie Comfort Level", font='small'
        ).pack()
        
        # Progress bar canvas
        self.progress_canvas = UIComponents.create_progress_canvas(progress_frame)
        self.progress_canvas.pack(fill='x', pady=(5, 0))
        
        # Hoodie recommendation text
        self.recommendation_label = UIComponents.create_styled_label(
            main_frame, text="Checking conditions...", 
            font='normal', color='accent_orange', wraplength=250, anchor='center'
        )
        self.recommendation_label.pack()
        
        # Last updated
        self.updated_label = UIComponents.create_styled_label(
            main_frame, text="", font='micro', color='text_muted', wraplength=250, anchor='center'
        )
        self.updated_label.pack(side='bottom')
        
    def draw_progress_bar(self, level):
        """Draw progress bar using UIComponents"""
        UIComponents.draw_progress_bar(self.progress_canvas, level)
        
    def get_location_and_weather(self):
        """Get user's location and weather data using the WeatherAPI module"""
        try:
            # Check if manual location is set
            if self.manual_location:
                lat = self.manual_location['lat']
                lon = self.manual_location['lon']
                city = self.manual_location['query']
                full_location = self.manual_location['display_name']
                
                print(f"Using manual location: {full_location}")
                
                # Get weather data for manual location
                weather_result = self.weather_api.get_weather_data(lat, lon)
                if weather_result.get('success'):
                    self.weather_data = weather_result
                    self.weather_data['city'] = city
                    self.weather_data['full_location'] = full_location
                    self.weather_data['coordinates'] = f"{lat:.3f}, {lon:.3f}"
                    self.weather_data['is_manual'] = True
                    self.update_display()
                else:
                    print(f"Weather API error for manual location: {weather_result.get('error')}")
                    self.use_demo_data()
                    
            else:
                # Auto-detect location
                location_result = self.weather_api.get_location_from_ip()
                if location_result.get('success'):
                    lat = location_result['lat']
                    lon = location_result['lon']
                    city = location_result['city']
                    region = location_result.get('region', '')
                    country = location_result.get('country', '')
                    
                    # Create full location string
                    location_parts = [city]
                    if region and region != city:
                        location_parts.append(region)
                    if country:
                        location_parts.append(country)
                    full_location = ', '.join(location_parts)
                    
                    # Get weather data
                    weather_result = self.weather_api.get_weather_data(lat, lon)
                    if weather_result.get('success'):
                        self.weather_data = weather_result
                        self.weather_data['city'] = city
                        self.weather_data['full_location'] = full_location
                        self.weather_data['coordinates'] = f"{lat:.3f}, {lon:.3f}"
                        self.weather_data['is_manual'] = False
                        self.update_display()
                    else:
                        print(f"Weather API error: {weather_result.get('error')}")
                        self.use_demo_data()
                else:
                    print(f"Location detection failed: {location_result.get('error')}")
                    self.use_demo_data()
                    
        except Exception as e:
            print(f"Error in get_location_and_weather: {e}")
            self.use_demo_data()
            
    def use_demo_data(self):
        """Use demo weather data when API is not available"""
        demo_data = self.weather_api.generate_demo_data()
        
        self.weather_data = demo_data
        self.weather_data['city'] = 'Demo Mode'
        self.weather_data['full_location'] = 'Demo Mode'
        self.weather_data['coordinates'] = '0.000, 0.000'
        self.weather_data['is_manual'] = False
        
        self.update_display()
        
    def calculate_hoodie_comfort(self):
        """Calculate hoodie comfort level using the HoodieComfortCalculator"""
        return self.hoodie_calculator.calculate_comfort_level(self.weather_data)
        
    def update_display(self):
        """Update the widget display with current weather data"""
        if not self.weather_data:
            return
            
        # Update location
        full_location = self.weather_data.get('full_location', 'Unknown')
        coordinates = self.weather_data.get('coordinates', '')
        is_manual = self.weather_data.get('is_manual', False)
        
        location_prefix = "📍" if not is_manual else "📌"  # Different icon for manual location
        location_text = f"{location_prefix} {full_location}"
        if is_manual:
            location_text += " (Manual)"
        
        self.location_label.config(text=location_text)
        
        # Update temperature
        temp = self.weather_data['main']['temp']
        self.temp_label.config(text=f"{temp:.1f}°C")
        
        # Update weather details
        humidity = self.weather_data['main']['humidity']
        wind_speed = self.weather_data['wind']['speed']
        description = self.weather_data['weather'][0]['description'].title()
        
        # Check for precipitation
        rain_text = ""
        if 'rain' in self.weather_data and self.weather_data['rain']:
            rain_mm = list(self.weather_data['rain'].values())[0]
            rain_text = f" | Rain: {rain_mm}mm"
        elif 'snow' in self.weather_data and self.weather_data['snow']:
            snow_mm = list(self.weather_data['snow'].values())[0]
            rain_text = f" | Snow: {snow_mm}mm"
            
        details_text = f"{description}\nHumidity: {humidity}% | Wind: {wind_speed} m/s{rain_text}"
        self.details_label.config(text=details_text)
        
        # Update hoodie recommendation
        comfort_level, recommendation = self.calculate_hoodie_comfort()
        self.draw_progress_bar(comfort_level)
        self.recommendation_label.config(text=recommendation)
        
        # Update timestamp with coordinates info
        current_time = datetime.now().strftime("%H:%M")
        coordinates = self.weather_data.get('coordinates', '')
        update_text = f"Updated: {current_time}"
        if coordinates and coordinates != '0.000, 0.000':
            update_text += f" | {coordinates}"
        self.updated_label.config(text=update_text)
        
    def start_weather_updates(self):
        """Start the weather update thread"""
        def update_weather():
            while True:
                self.get_location_and_weather()
                time.sleep(600)  # Update every 10 minutes
                
        weather_thread = threading.Thread(target=update_weather, daemon=True)
        weather_thread.start()
        
        # Initial update
        self.get_location_and_weather()
        
    def load_settings(self):
        """Load settings using SettingsManager"""
        settings = self.settings_manager.load_settings()
        self.manual_location = settings.get('manual_location')
        print(f"Loaded settings: manual_location = {self.manual_location}")
            
    def save_settings(self):
        """Save settings using SettingsManager"""
        settings = {
            'manual_location': self.manual_location
        }
        success = self.settings_manager.save_settings(settings)
        if success:
            print(f"Settings saved: {settings}")
        else:
            print("Failed to save settings")
            
    def open_settings(self):
        """Open the settings window with UIComponents styling"""
        settings_window = UIComponents.create_popup_window(self.root, "Weather Widget Settings", "400x800")
        
        # Position near the widget
        x = self.root.winfo_x() - 100
        y = self.root.winfo_y() + 50
        settings_window.geometry(f"400x500+{x}+{y}")
        
        # Title
        UIComponents.create_styled_label(
            settings_window, text="⚙ Settings", 
            font='title', bg='bg_secondary'
        ).pack(pady=10)
        
        # Location section
        location_frame = UIComponents.create_styled_frame(settings_window, bg='bg_secondary')
        location_frame.pack(fill='x', padx=20, pady=10)
        
        UIComponents.create_styled_label(
            location_frame, text="📍 Location Settings", 
            font='normal', color='accent_blue', bg='bg_secondary'
        ).pack(anchor='w')
        
        # Auto-detect vs Manual radio buttons
        self.location_mode = tk.StringVar()
        self.location_mode.set("auto" if not self.manual_location else "manual")
        
        auto_radio = tk.Radiobutton(location_frame, text="Auto-detect location (IP-based)", 
                                   variable=self.location_mode, value="auto",
                                   bg=UIComponents.COLORS['bg_secondary'], 
                                   fg='white', selectcolor=UIComponents.COLORS['bg_primary'],
                                   command=self.on_location_mode_change)
        auto_radio.pack(anchor='w', pady=5)
        
        manual_radio = tk.Radiobutton(location_frame, text="Manual location", 
                                     variable=self.location_mode, value="manual",
                                     bg=UIComponents.COLORS['bg_secondary'], 
                                     fg='white', selectcolor=UIComponents.COLORS['bg_primary'],
                                     command=self.on_location_mode_change)
        manual_radio.pack(anchor='w', pady=5)
        
        # Manual location input frame
        self.manual_frame = UIComponents.create_styled_frame(location_frame, bg='bg_secondary')
        self.manual_frame.pack(fill='x', pady=10)
        
        UIComponents.create_styled_label(
            self.manual_frame, text="City, Country (e.g., London, UK):", 
            font='small', color='text_secondary', bg='bg_secondary'
        ).pack(anchor='w')
        
        self.location_entry = UIComponents.create_styled_entry(self.manual_frame, width=30)
        self.location_entry.pack(anchor='w', pady=5)
        
        # Pre-fill with current manual location if set
        if self.manual_location:
            self.location_entry.insert(0, self.manual_location.get('query', ''))
        
        # Test location button
        test_btn = UIComponents.create_styled_button(
            self.manual_frame, text="Test Location", 
            command=self.test_manual_location, color='accent_orange'
        )
        test_btn.pack(anchor='w', pady=5)
        
        # Current location info
        info_frame = UIComponents.create_styled_frame(settings_window, bg='bg_secondary')
        info_frame.pack(fill='x', padx=20, pady=10)
        
        UIComponents.create_styled_label(
            info_frame, text="ℹ Current Location Info", 
            font='normal', color='accent_blue', bg='bg_secondary'
        ).pack(anchor='w')
        
        current_location = self.weather_data.get('full_location', 'Unknown')
        current_coords = self.weather_data.get('coordinates', 'Unknown')
        
        self.current_info_label = UIComponents.create_styled_label(
            info_frame, 
            text=f"Location: {current_location}\nCoordinates: {current_coords}",
            font='small', color='text_secondary', bg='bg_secondary', justify='left', wraplength=250
        )
        self.current_info_label.pack(anchor='w', pady=5)
        
        # Buttons frame
        buttons_frame = UIComponents.create_styled_frame(settings_window, bg='bg_secondary')
        buttons_frame.pack(fill='x', padx=20, pady=20)
        
        # Save button
        UIComponents.create_styled_button(
            buttons_frame, text="Save Settings", 
            command=lambda: self.save_settings_and_refresh(settings_window),
            color='accent_green', font='normal'
        ).pack(side='left', padx=5)
        
        # Cancel button
        UIComponents.create_styled_button(
            buttons_frame, text="Cancel", 
            command=settings_window.destroy,
            color='text_muted', font='normal'
        ).pack(side='left', padx=5)
        
        # Reset button
        UIComponents.create_styled_button(
            buttons_frame, text="Reset to Auto", 
            command=lambda: self.reset_to_auto(settings_window),
            color='accent_red', font='normal'
        ).pack(side='right', padx=5)
        
        # Update manual frame visibility
        self.on_location_mode_change()
        
    def on_location_mode_change(self):
        """Handle location mode radio button changes"""
        if self.location_mode.get() == "manual":
            for widget in self.manual_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Entry, tk.Button)):
                    widget.configure(state='normal')
        else:
            for widget in self.manual_frame.winfo_children():
                if isinstance(widget, (tk.Entry, tk.Button)):
                    widget.configure(state='disabled')
                    
    def test_manual_location(self):
        """Test the manually entered location"""
        location_query = self.location_entry.get().strip()
        if not location_query:
            tk.messagebox.showwarning("Invalid Input", "Please enter a location")
            return
            
        # Use WeatherAPI for geocoding
        geocode_result = self.weather_api.geocode_location(location_query)
        
        if geocode_result.get('success'):
            lat = geocode_result['lat']
            lon = geocode_result['lon']
            display_name = geocode_result['display_name']
            
            # Test weather data for this location
            weather_result = self.weather_api.get_weather_data(lat, lon)
            
            if weather_result.get('success'):
                temp = weather_result['main']['temp']
                result_msg = f"✓ Location found!\n\nName: {display_name}\nCoordinates: {lat:.3f}, {lon:.3f}\nCurrent Temperature: {temp}°C"
                tk.messagebox.showinfo("Location Test Successful", result_msg)
            else:
                tk.messagebox.showwarning("Weather Test Failed", 
                                        f"Location found but weather data unavailable.\n\nName: {display_name}\nCoordinates: {lat:.3f}, {lon:.3f}")
        else:
            error_msg = geocode_result.get('error', 'Unknown error')
            tk.messagebox.showerror("Location Not Found", 
                                  f"Could not find location: {location_query}\n\nError: {error_msg}\n\nTry a different format like:\n• London, UK\n• New York, USA\n• Tokyo, Japan")
            
    def save_settings_and_refresh(self, settings_window):
        """Save settings and refresh weather data"""
        if self.location_mode.get() == "manual":
            location_query = self.location_entry.get().strip()
            if not location_query:
                tk.messagebox.showwarning("Invalid Input", "Please enter a location or switch to auto-detect")
                return
                
            # Geocode the location using WeatherAPI
            geocode_result = self.weather_api.geocode_location(location_query)
            
            if geocode_result.get('success'):
                self.manual_location = {
                    'query': location_query,
                    'lat': geocode_result['lat'],
                    'lon': geocode_result['lon'],
                    'display_name': geocode_result['display_name']
                }
            else:
                error_msg = geocode_result.get('error', 'Unknown error')
                tk.messagebox.showerror("Error", f"Could not find location: {location_query}\n\nError: {error_msg}")
                return
        else:
            self.manual_location = None
            
        self.save_settings()
        settings_window.destroy()
        
        # Refresh weather data immediately
        self.get_location_and_weather()
        
    def reset_to_auto(self, settings_window):
        """Reset to auto-detect location"""
        self.manual_location = None
        self.save_settings()
        settings_window.destroy()
        self.get_location_and_weather()
        
    def show_location_info(self, event):
        """Show detailed location information on right-click"""
        if not self.weather_data:
            return
            
        coordinates = self.weather_data.get('coordinates', 'Unknown')
        full_location = self.weather_data.get('full_location', 'Unknown')
        is_manual = self.weather_data.get('is_manual', False)
        
        # Create a popup using UIComponents
        popup = UIComponents.create_popup_window(self.root, "Location Details", "350x230")
        
        # Position near the widget
        x = self.root.winfo_x() + 10
        y = self.root.winfo_y() + 100
        popup.geometry(f"350x230+{x}+{y}")
        
        # Content
        UIComponents.create_styled_label(
            popup, text="📍 Location Details", 
            font='title', bg='bg_secondary'
        ).pack(pady=10)
        
        mode_text = "Manual Location" if is_manual else "Auto-detected Location"
        UIComponents.create_styled_label(
            popup, text=f"Mode: {mode_text}", 
            font='small', color='accent_orange', bg='bg_secondary'
        ).pack(pady=2)
        
        UIComponents.create_styled_label(
            popup, text=f"Location: {full_location}", 
            font='small', color='text_secondary', bg='bg_secondary', wraplength=320
        ).pack(pady=2)
        
        UIComponents.create_styled_label(
            popup, text=f"Coordinates: {coordinates}", 
            font='small', color='text_secondary', bg='bg_secondary'
        ).pack(pady=2)
        
        # Close button
        UIComponents.create_styled_button(
            popup, text="Close", command=popup.destroy,
            color='accent_red', font='tiny'
        ).pack(pady=10)
        
        # Auto-close after 5 seconds
        popup.after(5000, popup.destroy)
        
    def get_alternative_weather(self, lat, lon):
        """Get weather from an alternative source for comparison (placeholder)"""
        # This functionality could be moved to WeatherAPI in the future
        # For now, just return None to avoid import dependencies
        return None
        
    def refresh_glass_background(self):
        """Refresh the progress bar (simplified version)"""
        if hasattr(self, 'weather_data') and self.weather_data:
            comfort_level, _ = self.calculate_hoodie_comfort()
            self.draw_progress_bar(comfort_level)
        
    def run(self):
        print("Starting main event loop...")
        self.root.mainloop()
        print("Main event loop ended.")

if __name__ == "__main__":
    print("Starting Weather Widget...")
    # Create the widget
    widget = WeatherWidget()
    print("Running widget...")
    widget.run()
    print("Widget finished.")
