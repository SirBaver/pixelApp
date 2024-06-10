#!/bin/bash

# Start Flask server
echo "Starting Flask server..."
python app.py &

# Start Redis server
echo "Starting Redis server..."
redis-server &

# Start Celery worker
echo "Starting Celery worker..."
celery -A app.celery worker --loglevel=info &

# Start Celery beat scheduler
echo "Starting Celery beat scheduler..."
celery -A app.celery beat --loglevel=info &

# Wait for all background jobs to complete
wait
