from kafka import KafkaConsumer
import json
import psycopg2
from sklearn.cluster import KMeans
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')
# DB_HOST = os.getenv('DB_HOST')
# DB_PORT = os.getenv('DB_PORT')  

def main():
    # # Connect to PostgreSQL
    # conn = psycopg2.connect(
    #     dbname=DB_NAME,
    #     user=DB_USER,
    #     password=DB_PASSWORD,
    #     host=DB_HOST,
    #     port=DB_PORT
    # )
    # cur = conn.cursor()

    # Kafka Consumer
    consumer = KafkaConsumer(
        'customer_data',
        bootstrap_servers='kafka:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )

    # Real-time segmentation
    customer_data = []
    for message in consumer:
        data = message.value
        print(data)
        # customer_data.append([data['SpendingScore'], data['AnnualIncome']])
        
        # if len(customer_data) >= 10:  # Process every 10 records
        #     kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        #     labels = kmeans.fit_predict(np.array(customer_data))
            
        #     # Store segmentation results
        #     for i, customer in enumerate(customer_data):
        #         cur.execute("""
        #             INSERT INTO customer_segments (CustomerID, SpendingScore, AnnualIncome, Segment)
        #             VALUES (%s, %s, %s, %s)
        #             ON CONFLICT (CustomerID) DO UPDATE SET Segment = EXCLUDED.Segment, LastUpdated = NOW();
        #         """, (data['CustomerID'], customer[0], customer[1], labels[i]))
            
        #     conn.commit()
        #     customer_data = []  # Reset batch

if __name__ == '__main__':
    main()
