from kafka import KafkaProducer
import json
import time
import random
import os
# Retrieve Kafka broker address from environment variable (default to 'kafka:9092')
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9093')

# Initialize Kafka producer with JSON serialization for message values
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
# Currently we don't have new datasets on engagements, so we create a synthetic one.
def generate_event():
    """Simulates a new engagement event"""
    campaign_id = random.randint(101, 200)
    income_category = random.choice(["Low Income", "Medium Income", "High Income"])
    target_audience = random.choice(["18-24", "25-34", "35-44", "45-54", "55+"])
    channel_used = random.choice(["Email", "Google Ads", "Instagram", "TikTok", "Website", "Landline", "Telephone"])
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