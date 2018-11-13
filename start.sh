#!/bin/bash
python manage.py celery worker --loglevel=info &
gunicorn -c audit/gun.config  audit.wsgi
