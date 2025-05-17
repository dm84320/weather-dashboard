import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WeatherScraper:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

    async def fetch_data(self, session: aiohttp.ClientSession, url: str, params: Dict = None) -> Dict:
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"Error fetching data from {url}: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Exception while fetching data from {url}: {str(e)}")
            return None

    async def get_coordinates(self, city: str) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.geocoding_url}?name={city}&count=1") as response:
                data = await response.json()
                if data.get("results"):
                    result = data["results"][0]
                    return {
                        "latitude": result["latitude"],
                        "longitude": result["longitude"],
                        "name": result["name"],
                        "country": result["country"]
                    }
                return None

    async def get_weather(self, lat: float, lon: float) -> Dict:
        async with aiohttp.ClientSession() as session:
            # Get current weather and hourly forecast
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,pressure_msl,weather_code",
                "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,pressure_msl,weather_code",
                "forecast_days": 3
            }
            async with session.get(f"{self.base_url}/forecast", params=params) as response:
                return await response.json()

    def get_weather_description(self, code: int) -> str:
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        return weather_codes.get(code, "Unknown")

    def get_weather_icon(self, code: int) -> str:
        icon_codes = {
            0: "☀️",  # Clear sky
            1: "🌤️",  # Mainly clear
            2: "⛅",   # Partly cloudy
            3: "☁️",   # Overcast
            45: "🌫️",  # Foggy
            48: "🌫️",  # Depositing rime fog
            51: "🌦️",  # Light drizzle
            53: "🌦️",  # Moderate drizzle
            55: "🌧️",  # Dense drizzle
            61: "🌧️",  # Slight rain
            63: "🌧️",  # Moderate rain
            65: "🌧️",  # Heavy rain
            71: "🌨️",  # Slight snow
            73: "🌨️",  # Moderate snow
            75: "🌨️",  # Heavy snow
            77: "🌨️",  # Snow grains
            80: "🌧️",  # Slight rain showers
            81: "🌧️",  # Moderate rain showers
            82: "🌧️",  # Violent rain showers
            85: "🌨️",  # Slight snow showers
            86: "🌨️",  # Heavy snow showers
            95: "⛈️",   # Thunderstorm
            96: "⛈️",   # Thunderstorm with slight hail
            99: "⛈️"    # Thunderstorm with heavy hail
        }
        return icon_codes.get(code, "❓")

    async def scrape_weather(self, city: str) -> Dict:
        coords = await self.get_coordinates(city)
        if not coords:
            return None

        weather_data = await self.get_weather(coords["latitude"], coords["longitude"])
        
        # Process current weather
        current = weather_data["current"]
        current_weather = {
            "source": "openmeteo",
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "wind_speed": current["wind_speed_10m"],
            "precipitation": current["precipitation"],
            "pressure": current["pressure_msl"],
            "weather_code": current["weather_code"],
            "description": self.get_weather_description(current["weather_code"]),
            "icon": self.get_weather_icon(current["weather_code"]),
            "location": f"{coords['name']}, {coords['country']}",
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "timestamp": datetime.now().isoformat()
        }

        # Process forecast
        hourly = weather_data["hourly"]
        forecast = []
        for i in range(0, len(hourly["time"]), 24):  # Get daily forecast
            if i < len(hourly["time"]):
                forecast.append({
                    "date": hourly["time"][i],
                    "temperature": hourly["temperature_2m"][i],
                    "humidity": hourly["relative_humidity_2m"][i],
                    "wind_speed": hourly["wind_speed_10m"][i],
                    "precipitation": hourly["precipitation"][i],
                    "pressure": hourly["pressure_msl"][i],
                    "weather_code": hourly["weather_code"][i],
                    "description": self.get_weather_description(hourly["weather_code"][i]),
                    "icon": self.get_weather_icon(hourly["weather_code"][i])
                })

        return {
            "current": current_weather,
            "forecast": forecast
        } 