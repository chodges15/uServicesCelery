#!/bin/bash

# turn on bash's job control
set -m

# Start the Flask frontend
python ./http_interface.py&

# Start the Celery worker for the frontend
celery --app=http_interface.celery worker --concurrency=10 --loglevel=INFO -Q http_queue
