#!/bin/bash
python manage.py celery worker --loglevel=info &

python manage.py runserver 0.0.0.0:8000

