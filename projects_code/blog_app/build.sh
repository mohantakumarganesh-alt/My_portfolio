#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn blog_project.wsgi:application --bind 0.0.0.0:$PORT
