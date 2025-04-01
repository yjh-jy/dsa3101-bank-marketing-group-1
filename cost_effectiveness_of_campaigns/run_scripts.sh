#!/bin/bash

echo "Starting analysis..."
docker exec -it cost_effectiveness_of_campaigns python3 scripts/cost_effectiveness.py
echo "Analysis ended"