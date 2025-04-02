from kafka import KafkaProducer
import json
import time
import random
import os
import psycopg2
import time
import pandas as pd

"""
Script helps to generate a new datapoint every 5 seconds, 
which is ingested by Kafka to be extracted in data_ingestion/real_time_data_ingestion.py
"""

print("Waiting for Kafka and postgres to be ready...")
time.sleep(10)  # Wait 10 seconds before connecting

# Retrieve Kafka broker address from environment variable (default to 'kafka:9092')
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')


# Initialize Kafka producer with JSON serialization for message values
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Load campaigns csv to ensure consistency
campaigns = pd.read_csv("../../app/data/processed/campaigns.csv")

# Construct mappings of campaign to channel to ensure consistency
CAMPAIGN_TO_CHANNEL = {
    "Affiliate Marketing": ["TikTok", "Instagram", "YouTube"],
    "Display Advertising": ["TikTok", "Instagram", "YouTube", "Google Ads", "Website"],
    "Search Engine Optimization": ["Google Ads"],
    "Email Marketing": ["Email"],
    "Telemarketing": ["Telephone", "Landline"],
}

# Currently we don't have new datasets on engagements, so we create a synthetic one.
def generate_event():
    """Simulates a new engagement event"""
    campaign_id = random.randint(1,99)
    campaign_type = campaigns.loc[campaigns["campaign_id"] == campaign_id, "campaign_type"].iloc[0]
    channel_used = random.choice(CAMPAIGN_TO_CHANNEL[campaign_type])
    income_category = random.choice(["Low Income", "Medium Income", "High Income"])
    target_audience = random.choice(["18-24", "25-34", "35-44", "45-54", "55+"])
    has_engaged = random.choice([1, 0])

    return {
        "campaign_id": campaign_id,
        "income_category": income_category,
        "target_audience": target_audience,
        "channel_used": channel_used,
        "has_engaged": has_engaged
    }

# Continuously send engagement events
while True:
    event = generate_event()
    producer.send("engagement_events", value=event)
    print(f"Sent event: {event}")
    time.sleep(3)  # Simulate event arrival rate