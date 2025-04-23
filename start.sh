#!/bin/bash

# Сборка статических файлов
python manage.py collectstatic --noinput

# Применение миграций
python manage.py migrate

# Запуск Gunicorn
gunicorn care_project.wsgi:application --bind 0.0.0.0:8000 