#!/bin/bash

echo "Start synthetic data generating..."

docker exec -it data python3 scripts/customer_generator.py
docker exec -it data python3 scripts/digital_usage_data_generator.py
docker exec -it data python3 scripts/engagement_details_generator.py
docker exec -it data python3 scripts/loan_data_generator.py  
docker exec -it data python3 scripts/products_owned_generator.py
docker exec -it data python3 scripts/transaction_campaign_generator.py

echo "Data generation ended"