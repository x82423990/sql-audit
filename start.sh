#!/bin/bash
python manage.py celery worker --loglevel=info &
gunicorn -c audit/gunicorn_config.py  audit.wsgi