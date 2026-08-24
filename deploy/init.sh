#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

sleep 1

echo "Applying migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
python3 main.py