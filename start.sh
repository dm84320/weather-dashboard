#!/bin/bash

# Change to the app directory
cd /app

# Initialize the database
echo "Initializing database..."
python -c "from app.core.init_db import init_db; init_db()"

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 