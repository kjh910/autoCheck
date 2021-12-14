#!/bin/sh

python manage.py migrate

python manage.py collectstatic --noinput

# python manage.py runserver 0.0.0.0:80

gunicorn --bind 0.0.0.0:80 config.wsgi:application --workers 3