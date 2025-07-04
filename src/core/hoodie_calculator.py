"""
Hoodie comfort calculator module.
Contains logic for determining hoodie comfort levels based on weather conditions.
"""


class HoodieComfortCalculator:
    """Calculate hoodie comfort levels based on weather data"""

    def __init__(self):
        # Temperature ranges (in Celsius)
        self.temp_ranges = {
            "perfect": (10, 15),  # Perfect hoodie weather
            "great": (5, 22),  # Great for hoodie
            "good": (0, 28),  # Good for hoodie
            "warm": (28, 35),  # Getting warm
            "hot": (35, float("inf")),  # Too hot
        }

        # Comfort messages
        self.messages = {
            "perfect": "Perfect hoodie weather! 👍",
            "great": "Great for a hoodie! 😊",
            "good": "Good for a light hoodie 👌",
            "warm": "A bit warm for a hoodie 🌡️",
            "hot": "Too hot for a hoodie ☀️",
            "cold": "Perfect for a thick hoodie! 🧥",
            "freezing": "Bundle up! Extra layers needed! ❄️",
        }

    def calculate_comfort_level(self, weather_data):
        """
        Calculate hoodie comfort level based on weather conditions.
        Returns tuple: (comfort_score, recommendation_text)
        comfort_score: 0.0 = perfect for hoodie, 1.0 = not suitable
        """
        if not weather_data:
            return 0.5, "Checking conditions..."

        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        # Check for precipitation
        has_rain = "rain" in weather_data and weather_data["rain"]
        has_snow = "snow" in weather_data and weather_data["snow"]

        # Calculate base comfort score based on temperature
        comfort_score = self._calculate_temperature_score(temp)

        # Apply wind factor (wind makes it feel cooler)
        comfort_score = self._apply_wind_factor(comfort_score, wind_speed)

        # Apply precipitation factor
        comfort_score = self._apply_precipitation_factor(
            comfort_score, has_rain, has_snow
        )

        # Apply humidity factor
        comfort_score = self._apply_humidity_factor(comfort_score, humidity)

        # Clamp between 0 and 1
        comfort_score = max(0.0, min(1.0, comfort_score))

        # Generate recommendation text
        recommendation = self._generate_recommendation(
            temp, comfort_score, has_rain, has_snow
        )

        return comfort_score, recommendation

    def _calculate_temperature_score(self, temp):
        """Calculate base comfort score from temperature"""
        if temp < -5:
            return 0.0  # Freezing - perfect for thick hoodie
        elif temp < 0:
            return 0.1  # Very cold - great for hoodie
        elif temp < 10:
            return 0.15  # Cold - perfect for hoodie
        elif temp < 15:
            return 0.2  # Cool - great for hoodie
        elif temp < 22:
            return 0.3  # Mild - good for light hoodie
        elif temp < 28:
            return 0.7  # Warm - getting uncomfortable
        elif temp < 35:
            return 0.85  # Hot - not suitable
        else:
            return 0.95  # Very hot - definitely not suitable

    def _apply_wind_factor(self, score, wind_speed):
        """Apply wind correction to comfort score"""
        if wind_speed > 10:
            return score - 0.2  # Strong wind makes hoodie more comfortable
        elif wind_speed > 5:
            return score - 0.1  # Moderate wind
        return score

    def _apply_precipitation_factor(self, score, has_rain, has_snow):
        """Apply precipitation correction to comfort score"""
        if has_snow:
            return score - 0.15  # Snow makes hoodie more desirable
        elif has_rain:
            return score - 0.1  # Light rain good for hoodie
        return score

    def _apply_humidity_factor(self, score, humidity):
        """Apply humidity correction to comfort score"""
        if humidity > 85:
            return score + 0.15  # Very high humidity makes hoodie uncomfortable
        elif humidity > 75:
            return score + 0.1  # High humidity
        return score

    def _generate_recommendation(self, temp, comfort_score, has_rain, has_snow):
        """Generate human-readable recommendation text"""
        # Special cases for extreme weather
        if temp < -10:
            return self.messages["freezing"]
        elif temp < 0:
            return self.messages["cold"]
        elif has_snow:
            return "Perfect hoodie weather for snow! ❄️🧥"
        elif has_rain and temp < 20:
            return "Great hoodie weather for rain! 🌧️👍"

        # Standard recommendations based on comfort score
        if comfort_score < 0.25:
            return self.messages["perfect"]
        elif comfort_score < 0.4:
            return self.messages["great"]
        elif comfort_score < 0.6:
            return self.messages["good"]
        elif comfort_score < 0.8:
            return self.messages["warm"]
        else:
            return self.messages["hot"]

    def get_comfort_category(self, comfort_score):
        """Get comfort category from score"""
        if comfort_score < 0.33:
            return "excellent"
        elif comfort_score < 0.66:
            return "good"
        else:
            return "poor"

    def get_detailed_analysis(self, weather_data):
        """Get detailed comfort analysis"""
        if not weather_data:
            return "No weather data available"

        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        analysis = []

        # Temperature analysis
        if temp < 5:
            analysis.append("🌡️ Cold temperature - perfect for hoodie")
        elif temp < 20:
            analysis.append("🌡️ Mild temperature - good for hoodie")
        elif temp < 30:
            analysis.append("🌡️ Warm temperature - light hoodie only")
        else:
            analysis.append("🌡️ Hot temperature - avoid hoodie")

        # Wind analysis
        if wind_speed > 7:
            analysis.append("💨 Windy conditions - hoodie recommended")
        elif wind_speed > 3:
            analysis.append("💨 Light breeze - hoodie comfortable")

        # Humidity analysis
        if humidity > 80:
            analysis.append("💧 High humidity - may feel stuffy in hoodie")
        elif humidity < 30:
            analysis.append("💧 Low humidity - hoodie very comfortable")

        # Precipitation analysis
        if "rain" in weather_data:
            analysis.append("🌧️ Rain detected - hoodie provides good coverage")
        if "snow" in weather_data:
            analysis.append("❄️ Snow conditions - hoodie highly recommended")

        return (
            "\n".join(analysis) if analysis else "Standard conditions for hoodie wear"
        )
