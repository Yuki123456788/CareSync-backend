#!/bin/bash

python manage.py makemigrations
python manage.py migrate
gunicorn -b :8000 config.wsgi:application --timeout 120
