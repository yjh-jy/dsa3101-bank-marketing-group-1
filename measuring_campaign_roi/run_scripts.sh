#!/bin/bash

echo "Starting analysis..."
docker exec -it measuring_campaign_roi python3 scripts/main.py
echo "Analysis ended"