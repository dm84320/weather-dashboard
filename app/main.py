from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.core.init_db import init_db

app = FastAPI(
    title="Weather Dashboard API",
    description="API for weather data scraping and visualization",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/")
async def root():
    return {"message": "Welcome to Weather Dashboard API"}

# Import and include routers
from app.api.endpoints import weather, sources

app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(sources.router, prefix="/api/sources", tags=["sources"]) 