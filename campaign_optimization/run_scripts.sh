#!/bin/bash

echo "Starting analysis..."

echo "Starting real_time_data_generation.py ..."
docker exec -d campaign_optimization python3 scripts/data_generation/real_time_data_generation.py

echo "Starting real_time_data_ingestion.py ..."
docker exec -d campaign_optimization python3 scripts/data_ingestion/real_time_data_ingestion.py

echo "Starting data_ingestion_initial.py ..."
docker exec -d campaign_optimization python3 scripts/data_ingestion_initial.py

echo "Starting campaign_optimization.py ..."
docker exec -d campaign_optimization python3 scripts/campaign_optimization.py

echo "Starting campaign_suggestion.py ..."
docker exec -it campaign_optimization python campaign_suggestion.py

echo "Analysis ended"