#!/bin/bash
set -e

echo "Starting application..."

# Create directories if they don't exist
mkdir -p /app/static
mkdir -p /app/media
mkdir -p /app/staticfiles

# Set permissions
chmod -R 755 /app/static
chmod -R 755 /app/media
chmod -R 755 /app/staticfiles

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn care_project.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120 