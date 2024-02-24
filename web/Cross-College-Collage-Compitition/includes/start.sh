#!/bin/bash
gunicorn -t 600 --workers=3 -b 127.0.0.1:8001 --chdir /application/ c:app &
gunicorn -t 600 --workers=3 -b 0.0.0.0:8000 --chdir /application/ app:app
# python -u app.py &
# python -u c.py
