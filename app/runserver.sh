#!/bin/sh

python manage.py migrate

python manage.py collectstatic --noinput

# python3 manage.py runserver 0.0.0.0:8001

gunicorn --bind 0.0.0.0:8000 config.wsgi