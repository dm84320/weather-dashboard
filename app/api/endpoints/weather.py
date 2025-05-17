from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.weather import WeatherData
from app.scrapers.weather_scraper import WeatherScraper
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

router = APIRouter()
scraper = WeatherScraper()

@router.get("/current")
async def get_current_weather(city: str, db: Session = Depends(get_db)):
    weather_data = await scraper.scrape_weather(city)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    # Store current weather in database
    current = weather_data["current"]
    db_weather = WeatherData(
        source=current["source"],
        temperature=current["temperature"],
        humidity=current["humidity"],
        wind_speed=current["wind_speed"],
        precipitation=current["precipitation"],
        pressure=current["pressure"],
        description=current["description"],
        location=current["location"],
        timestamp=datetime.fromisoformat(current["timestamp"])
    )
    db.add(db_weather)
    db.commit()
    
    return weather_data

@router.get("/historical")
async def get_historical_weather(city: str, db: Session = Depends(get_db)):
    weather_data = db.query(WeatherData).filter(
        WeatherData.location.like(f"%{city}%")
    ).order_by(WeatherData.timestamp.desc()).limit(10).all()
    
    if not weather_data:
        raise HTTPException(status_code=404, detail="Historical weather data not found")
    
    return weather_data

@router.get("/sources")
async def get_available_sources():
    return list(scraper.sources.keys()) 