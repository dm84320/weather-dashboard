from fastapi import APIRouter
from app.scrapers.weather_scraper import WeatherScraper

router = APIRouter()
scraper = WeatherScraper()

@router.get("/")
async def get_sources():
    """
    Get list of available weather data sources
    """
    return {
        "sources": list(scraper.sources.keys()),
        "description": "List of available weather data sources that can be used to fetch weather information"
    } 