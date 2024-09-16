#!/bin/sh

# Wait for the database to be ready and run the migration script
echo "Running migrations..."
python3 app/migrations.py

# Check the exit status of the migration script
if [ $? -ne 0 ]; then
  echo "Migration failed. Exiting."
  exit 1
fi

# Start the FastAPI server in the background
echo "Starting the web server..."

uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000 & SERVER_PID=$!

# Wait for the server to be ready
echo "Waiting for the server to be ready..."
while ! curl -sSf http://localhost:8000/ping; do
  echo "Server is not up yet. Waiting..."
  sleep 2
done

# POST data.csv to the FastAPI endpoint to upload batch
echo "Uploading data to the server..."
curl -X 'POST' \
  'http://localhost:8000/videos/batch/csv' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/app/data.csv;type=text/csv'

# Check the exit status of the curl command
if [ $? -ne 0 ]; then
  echo "Data upload failed. Exiting."
  exit 1
fi

# Wait for the FastAPI server process to finish
wait $SERVER_PID
