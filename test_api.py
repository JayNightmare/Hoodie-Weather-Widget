#!/usr/bin/env python3
"""
Quick test script to verify the Open-Meteo API integration
"""
import requests

def test_weather_api():
    print("Testing Open-Meteo API integration...")
    
    try:
        # Get location
        print("1. Getting location...")
        location_response = requests.get('http://ip-api.com/json/', timeout=10)
        location_data = location_response.json()
        
        if location_data['status'] == 'success':
            lat = location_data['lat']
            lon = location_data['lon']
            city = location_data['city']
            print(f"   Location: {city} ({lat}, {lon})")
            
            # Get weather
            print("2. Getting weather data...")
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m&hourly=precipitation&timezone=auto&forecast_days=1"
            weather_response = requests.get(weather_url, timeout=10)
            
            if weather_response.status_code == 200:
                data = weather_response.json()
                current = data['current']
                
                print("   ✓ Weather data received successfully!")
                print(f"   Temperature: {current['temperature_2m']}°C")
                print(f"   Humidity: {current['relative_humidity_2m']}%")
                print(f"   Wind: {current['wind_speed_10m']} m/s")
                print(f"   Precipitation: {current['precipitation']} mm")
                print(f"   Weather code: {current['weather_code']}")
                
                return True
            else:
                print(f"   ✗ Weather API error: {weather_response.status_code}")
                return False
        else:
            print(f"   ✗ Location error: {location_data}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_weather_api()
    if success:
        print("\n🎉 All tests passed! The widget should work with live weather data.")
    else:
        print("\n❌ Tests failed. The widget will fall back to demo data.")
