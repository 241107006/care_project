#!/bin/bash
set -e

# Create necessary directories if they don't exist
mkdir -p /app/static
mkdir -p /app/media
mkdir -p /app/staticfiles

# Set proper permissions
chmod -R 755 /app/static
chmod -R 755 /app/media
chmod -R 755 /app/staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Apply migrations
python manage.py migrate

# Start Gunicorn
exec gunicorn care_project.wsgi:application --bind 0.0.0.0:8000 