#!/bin/bash

echo "Starting analysis..."
docker exec -it customer_retention_strategies python3 scripts/customer_retention_strategies.py
echo "Analysis ended"