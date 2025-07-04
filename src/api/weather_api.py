"""
Weather API module for fetching weather data from various sources.
"""

import json
import random
import time

import requests


class WeatherAPI:
    """Handle weather data fetching from different APIs"""

    def __init__(self):
        self.timeout = 10

    def get_location_from_ip(self):
        """Get user's location based on IP address"""
        try:
            response = requests.get("http://ip-api.com/json/", timeout=self.timeout)
            data = response.json()

            if data["status"] == "success":
                return {
                    "lat": data["lat"],
                    "lon": data["lon"],
                    "city": data["city"],
                    "region": data.get("regionName", ""),
                    "country": data.get("country", ""),
                    "success": True,
                }
            return {"success": False, "error": "Location detection failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def geocode_location(self, location_query):
        """Geocode a location string to coordinates using OpenStreetMap"""
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={location_query}&format=json&limit=1"
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": "HoodieWeatherWidget/1.0"},
            )

            if response.status_code == 200:
                data = response.json()
                if data:
                    location = data[0]
                    return {
                        "lat": float(location["lat"]),
                        "lon": float(location["lon"]),
                        "display_name": location["display_name"],
                        "success": True,
                    }
            return {"success": False, "error": "Location not found"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_weather_data(self, lat, lon):
        """Fetch weather data from Open-Meteo API"""
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&"
                f"current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&"
                f"hourly=precipitation&timezone=auto&forecast_days=1"
            )

            response = requests.get(url, timeout=self.timeout)

            if response.status_code == 200:
                api_data = response.json()
                current = api_data["current"]

                weather_data = {
                    "main": {
                        "temp": current["temperature_2m"],
                        "humidity": current["relative_humidity_2m"],
                    },
                    "wind": {
                        "speed": round(
                            current["wind_speed_10m"] / 3.6, 1
                        )  # Convert km/h to m/s
                    },
                    "weather": [
                        {
                            "main": self.get_weather_description(
                                current["weather_code"]
                            ),
                            "description": self.get_weather_description(
                                current["weather_code"]
                            ).lower(),
                        }
                    ],
                    "success": True,
                }

                # Add precipitation if present
                if current["precipitation"] > 0:
                    weather_data["rain"] = {"1h": current["precipitation"]}

                return weather_data

            return {"success": False, "error": f"API error: {response.status_code}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_weather_description(self, weather_code):
        """Convert Open-Meteo weather codes to descriptions"""
        weather_codes = {
            0: "Clear Sky",
            1: "Mainly Clear",
            2: "Partly Cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing Rime Fog",
            51: "Light Drizzle",
            53: "Moderate Drizzle",
            55: "Dense Drizzle",
            56: "Light Freezing Drizzle",
            57: "Dense Freezing Drizzle",
            61: "Slight Rain",
            63: "Moderate Rain",
            65: "Heavy Rain",
            66: "Light Freezing Rain",
            67: "Heavy Freezing Rain",
            71: "Slight Snow",
            73: "Moderate Snow",
            75: "Heavy Snow",
            77: "Snow Grains",
            80: "Slight Rain Showers",
            81: "Moderate Rain Showers",
            82: "Violent Rain Showers",
            85: "Slight Snow Showers",
            86: "Heavy Snow Showers",
            95: "Thunderstorm",
            96: "Thunderstorm with Slight Hail",
            99: "Thunderstorm with Heavy Hail",
        }
        return weather_codes.get(weather_code, "Unknown")

    def generate_demo_data(self):
        """Generate demo weather data when API is not available"""
        base_temp = 15 + (time.time() % 86400) / 86400 * 10

        demo_data = {
            "main": {
                "temp": round(base_temp + random.uniform(-2, 2), 1),
                "humidity": random.randint(45, 85),
            },
            "wind": {"speed": round(random.uniform(1, 8), 1)},
            "weather": [{"main": "Demo", "description": "demo weather data"}],
            "success": True,
            "is_demo": True,
        }

        # Simulate precipitation occasionally
        if random.random() < 0.3:
            demo_data["rain"] = {"1h": round(random.uniform(0.1, 2.0), 1)}

        return demo_data
