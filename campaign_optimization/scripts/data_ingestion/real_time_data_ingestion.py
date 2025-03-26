from kafka import KafkaConsumer
import json
import os
import psycopg2

# Retrieve Kafka broker address
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')

# PostgreSQL connection details
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "dsa3101project"
DB_HOST = "postgres"
DB_PORT = "5432"

# Initialize Kafka consumer
consumer = KafkaConsumer(
    "engagement_events",
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset="earliest",
    enable_auto_commit=True
)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()


# Consume messages and insert into PostgreSQL
for message in consumer:
    event = message.value
    print(f"Received event: {event}")

    # Insert data into the table
    cur.execute("""
        INSERT INTO Engagements (campaign_id, income_category, target_audience, channel_used, has_engaged)
        VALUES (%s, %s, %s, %s, %s)
    """, (event["campaign_id"], event["income_category"], event["target_audience"], event["channel_used"], event["has_engaged"]))
    
    conn.commit()

# Close resources (this won't execute unless the loop is stopped)
cur.close()
conn.close()
