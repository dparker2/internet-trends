#!/bin/sh

echo "what"

python3 test/me.py &
gunicorn --reload -b 0.0.0.0:8080 app.main:app
