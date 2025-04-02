#!/bin/bash

echo "Starting analysis..."
docker exec -it campaign_impact_analysis python3 scripts/campaign_impact_analysis.py
echo "Analysis ended"