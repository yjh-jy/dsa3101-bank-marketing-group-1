#!/bin/bash

echo "Starting analysis..."
docker exec -it behavioural_patterns python3 scripts/behavioural_patterns.py
echo "Analysis ended"