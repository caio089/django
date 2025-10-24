#!/usr/bin/env bash
# Exit on any error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Test Supabase connection
echo "Testing Supabase connection..."
python teste_supabase.py

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput

echo "Build completed successfully with Supabase!"
