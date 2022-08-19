#!/bin/bash
python3 manage.py migrate

gunicorn ideas.wsgi --bind 0.0.0.0:8000 -D
daphne -b 0.0.0.0 -p 8001 ideas.asgi:application
