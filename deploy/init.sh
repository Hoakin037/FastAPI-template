#!/bin/bash

echo "Waiting for PostgreSQL to be ready..."

sleep 1

echo "Applying migrations..."
alembic upgrade head

echo "Starting Uvicorn..."
uvicorn main:app --host 0.0.0.0 --port 8006