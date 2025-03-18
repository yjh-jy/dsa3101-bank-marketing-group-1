from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_customer_data():
    return {
        "CustomerID": random.randint(1000, 9999),
        "SpendingScore": random.uniform(0, 100),
        "AnnualIncome": random.randint(20000, 100000),
        "Timestamp": time.time()
    }

while True:
    data = generate_customer_data()
    producer.send('customer_data', value=data)
    print(f"Sent: {data}")
    time.sleep(2)  # Simulates real-time transactions every 2 seconds
