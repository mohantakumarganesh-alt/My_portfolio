#!/bin/bash
# Install requirements
pip install -r requirements.txt

# Run Django commands
python manage.py collectstatic --noinput
python manage.py migrate
