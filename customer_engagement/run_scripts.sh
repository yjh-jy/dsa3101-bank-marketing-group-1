#!/bin/bash

echo "Starting analysis..."
docker exec -it customer_engagement python3 scripts/customer_engagement.py
docker exec -it customer_engagement python3 scripts/campaign_engagement.py
echo "Analysis ended"