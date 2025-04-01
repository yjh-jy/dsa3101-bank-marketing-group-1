#!/bin/bash

echo "Starting analysis..."
docker exec -it predicting_customer_preference python3 scripts/main.py
echo "Analysis ended"