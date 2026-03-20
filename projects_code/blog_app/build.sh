#!/bin/bash
# Install requirements
pip install -r requirements.txt

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate

# Seed Site domain and Google SocialApp in production DB
python manage.py setup_social_auth
