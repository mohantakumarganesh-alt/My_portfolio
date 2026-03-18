#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
# build.sh handles only build-time setups (collectstatic, migrate)
