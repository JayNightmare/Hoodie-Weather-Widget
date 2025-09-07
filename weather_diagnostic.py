#!/usr/bin/env python3
"""
Weather Diagnostic Tool
Compares weather data from different sources and shows location detection accuracy
"""
import json
import sys
from datetime import datetime

import requests


def get_location_info():
    """Get detailed location information"""
    print("🔍 Detecting location...")
    try:
        # Primary location service
        response = requests.get("http://ip-api.com/json/", timeout=10)
        data = response.json()

        if data["status"] == "success":
            print(f"[GOOD] Location detected successfully:")
            print(f"  City: {data['city']}")
            print(f"  Region: {data.get('regionName', 'N/A')}")
            print(f"  Country: {data.get('country', 'N/A')}")
            print(f"  Coordinates: {data['lat']:.4f}, {data['lon']:.4f}")
            print(f"  ISP: {data.get('isp', 'N/A')}")
            print(f"  Timezone: {data.get('timezone', 'N/A')}")
            return data["lat"], data["lon"], data["city"]
        else:
            print(f"[ERROR] Location detection failed: {data}")
            return None, None, None

    except Exception as e:
        print(f"[ERROR] Error getting location: {e}")
        return None, None, None


def get_openmeteo_weather(lat, lon):
    """Get weather from Open-Meteo"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&timezone=auto&forecast_days=1"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            current = data["current"]
            return {
                "source": "Open-Meteo",
                "temperature": current["temperature_2m"],
                "humidity": current["relative_humidity_2m"],
                "wind_speed_kmh": current["wind_speed_10m"],
                "wind_speed_ms": round(current["wind_speed_10m"] / 3.6, 1),
                "precipitation": current["precipitation"],
                "weather_code": current["weather_code"],
                "timestamp": current["time"],
            }
    except Exception as e:
        print(f"[ERROR] Open-Meteo error: {e}")
    return None


def get_weather_comparison(lat, lon):
    """Compare weather data from different sources"""
    print(f"\nComparing weather data for coordinates: {lat:.4f}, {lon:.4f}")
    print("-" * 60)

    # Open-Meteo
    openmeteo = get_openmeteo_weather(lat, lon)
    if openmeteo:
        print(f"{openmeteo['source']}:")
        print(f"  Temperature: {openmeteo['temperature']}°C")
        print(f"  Humidity: {openmeteo['humidity']}%")
        print(
            f"  Wind: {openmeteo['wind_speed_ms']} m/s ({openmeteo['wind_speed_kmh']} km/h)"
        )
        print(f"  Precipitation: {openmeteo['precipitation']} mm")
        print(f"  Last updated: {openmeteo['timestamp']}")

    # Could add more weather sources here for comparison
    print("\nNote: Temperature differences between services are normal due to:")
    print("  - Different weather station networks")
    print("  - Different update frequencies")
    print("  - Different data processing methods")
    print("  - Micro-climate variations")


def main():

    print("=" * 60)
    print("HOODIE WEATHER WIDGET - DIAGNOSTIC TOOL")
    print("=" * 60)

    # Check for test mode
    test_mode = "--test" in sys.argv
    if test_mode:
        print("[TEST MODE] Using mock location for diagnostic tests.")
        # Mock location: New York City
        lat, lon, city = 40.7128, -74.0060, "New York"
    else:
        # Get location
        lat, lon, city = get_location_info()

    if lat and lon:
        # Get weather comparison
        get_weather_comparison(lat, lon)

        print(f"\nAccuracy Check:")
        print(f"  If this location is incorrect, the temperature difference")
        print(f"  might be due to measuring weather for the wrong area.")
        print(f"  Expected location: {city}")
        print(f"  If this doesn't match your actual location, consider")
        print(f"  using a VPN or checking your IP location settings.")

    print(f"\nDiagnostic completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
