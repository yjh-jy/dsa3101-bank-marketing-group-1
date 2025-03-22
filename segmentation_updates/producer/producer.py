from datetime import datetime
from kafka import KafkaProducer
import json
import random
import time
import os

# Retrieve Kafka broker address from environment variable (default to 'kafka:9092')
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')

# Initialize Kafka producer with JSON serialization for message values
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_customer_data(i):
    """
    Generate simulated transaction data for a customer.

    Args:
        i (int): A transaction identifier that increments with each call.

    Returns:
        dict: A dictionary containing transaction details.
    """
    return {
        "transaction_id": i,
        "customer_id": random.randint(1, 4000),  # Random customer ID between 1 and 4000
        "transaction_type": random.choice(['Credit', 'Withdrawal', 'Transfer', 'Deposit']),
        "transaction_amt": random.randint(1, 5000),  # Random transaction amount
        "transaction_date": datetime.now().isoformat()  # Current timestamp in ISO format
    }

def main():
    """
    Continuously generate and send simulated transaction data to the Kafka topic 'customer_data'.
    """
    i = 1  # Initialize transaction counter
    while True:
        i += 1
        data = generate_customer_data(i)
        producer.send('customer_data', value=data)
        print(f"Sent: {data}")  # Log the sent data
        time.sleep(2)  # Wait for 2 seconds before sending the next transaction

if __name__ == '__main__':
    main()
