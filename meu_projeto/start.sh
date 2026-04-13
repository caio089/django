#!/usr/bin/env bash
# Exit on any error
set -o errexit

# Run database migrations
python manage.py migrate --noinput

# Start the application
gunicorn meu_projeto.wsgi:application --bind 0.0.0.0:$PORT
