#!/bin/bash
gunicorn -c audit/gunicorn_config.py  audit.wsgi
python manage.py celery worker --loglevel=info