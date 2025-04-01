#!/bin/bash

echo "Starting analysis..."
docker exec -it customer_segmentation python3 scripts/segmentation.py
echo "Analysis ended"