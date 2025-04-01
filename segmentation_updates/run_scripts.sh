#!/bin/bash

echo "Starting analysis..."

echo "Running producer script...."
docker exec -d segmentation_updates python3 producer/producer.py
echo "Producer script started"

echo "Running consumer script...."
docker exec -d segmentation_updates python3 consumer/consumer.py
echo "Producer script started"

echo "Running Dash Frontend and Flask API script...."
docker exec -d segmentation_updates python3 api/app.py
echo "Dash Frontend and Flask API script started"

echo "All scripts ran for segmentation_updates"
echo "Please access the dashboard at:  http://localhost:5001/dashboard/"

echo "Analysis ended"