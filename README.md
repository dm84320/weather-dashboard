# Weather Dashboard

A modern weather dashboard application that provides current weather conditions, forecasts, and historical data.

## Features
- Current weather data
- 3-day forecast
- Historical weather data
- City comparison
- Interactive weather map
- Weather alerts and notifications
- Air quality information
- UV index
- Clothing suggestions
- Activity recommendations

## API Documentation
The API documentation is available at `/docs` when running the application.

### Available Endpoints
- `GET /api/weather/current?city={city}` - Get current weather for a city
- `GET /api/weather/historical?city={city}` - Get historical weather data
- `GET /api/weather/forecast?city={city}` - Get weather forecast
- `GET /api/weather/compare?city1={city1}&city2={city2}` - Compare weather between two cities

## Setup
1. Clone the repository
```bash
git clone https://github.com/yourusername/weather-dashboard.git
cd weather-dashboard
```

2. Run with Docker Compose
```bash
docker-compose up --build
```

3. Access the application at `http://localhost:8000`

## Technologies Used
- Frontend: HTML, CSS, JavaScript, Bootstrap
- Backend: FastAPI, SQLAlchemy
- Database: SQLite
- Maps: Leaflet.js
- Weather Data: OpenMeteo API

## Development
1. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
uvicorn app.main:app --reload
```

## Project Structure
```
weather-dashboard/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── weather.py
│   ├── core/
│   │   └── init_db.py
│   ├── models/
│   │   └── weather.py
│   ├── scrapers/
│   │   └── weather_scraper.py
│   ├── static/
│   │   └── index.html
│   └── main.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 