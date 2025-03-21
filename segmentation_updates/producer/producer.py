from kafka import KafkaProducer
import json
import random
import time
import os

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulating transactions coming in for each customers
def generate_customer_data(i):
    return {
        "transaction_id": i,
        "customer_id": random.randint(1, 4000),
        "transaction_type": random.choice(['Credit', 'Withdrawal', 'Transfer', 'Deposit']),
        "transaction_amt": random.randint(1, 5000),
        "transaction_date": time.time()
    }

def main():
    i = 999821
    while True:
        i += 1
        data = generate_customer_data(i)
        producer.send('customer_data', value=data)
        print(f"Sent: {data}")
        time.sleep(1)  # Simulates real-time transactions every 1 seconds

if __name__ == '__main__':
    main()
