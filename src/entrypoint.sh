#!/bin/bash

echo "migrate"
python3 manage.py migrate

# Start server
echo "Starting server"
nginx -g "daemon on;" && uwsgi --ini ./CyCarrier/uwsgi.ini
