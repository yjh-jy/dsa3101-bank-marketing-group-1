import time
from kafka import KafkaConsumer
import json
import pandas as pd
import psycopg2
from psycopg2 import pool
from sklearn.cluster import KMeans
import numpy as np
import os
from dotenv import load_dotenv
from datetime import datetime

from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import RobustScaler
from scipy.stats.mstats import winsorize

# Load environment variables from .env file
load_dotenv()

# Kafka and database configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "dsa3101project"
DB_HOST = "postgres"
DB_PORT = "5433"

# Micro-batching parameters: control the time window and maximum batch size for processing transactions.
MICRO_BATCH_WINDOW = 0.1  # 100ms time window
MAX_BATCH_SIZE = 10       # Maximum transactions to accumulate before processing

def fetch_customer_data(conn):
    """
    Fetch customer data for clustering from the customer_segments table.

    Args:
        conn (psycopg2.connection): A connection object to the database.

    Returns:
        pd.DataFrame: DataFrame containing customer data.
    """
    query = """
        SELECT customer_id, income, balance, customer_lifetime_value, debt, tenure, 
               credit_default, days_from_last_transaction, avg_transaction_amt, 
               num_transactions, digital_engagement_score, loan_repayment_time, 
               total_products_owned, has_loan 
        FROM customer_segments
    """
    df = pd.read_sql(query, conn)
    return df

def recalculate_clusters(df):
    """
    Perform KMeans clustering on the customer data and assign segments based on cluster ranking.

    Args:
        df (pd.DataFrame): DataFrame containing customer features.

    Returns:
        pd.DataFrame: DataFrame with customer_id and assigned segment.
    """
    features_to_scale = [
        "income", "balance", "debt", "customer_lifetime_value", "days_from_last_transaction",
        "avg_transaction_amt", "digital_engagement_score", "total_products_owned", 
        "loan_repayment_time", "num_transactions"
    ]
    robust_features = ["income", "balance", "debt", "customer_lifetime_value", "avg_transaction_amt"]
    # Apply winsorization to reduce the impact of outliers; modifies df in-place.
    for col in robust_features:
        df[col] = pd.Series(winsorize(df[col].to_numpy(), limits=[0.05, 0.05]))

    standard_features = [
        "days_from_last_transaction", "digital_engagement_score", 
        "total_products_owned", "loan_repayment_time", "num_transactions"
    ]

    # Create a scaled copy of the data
    scalerrobust = RobustScaler()
    df_scaled = df.copy()
    df_scaled[robust_features] = scalerrobust.fit_transform(df[robust_features])

    scaler_standard = StandardScaler()
    df_scaled[standard_features] = scaler_standard.fit_transform(df[standard_features])

    # Perform KMeans clustering
    optimal_k = 3
    df_scaled["Cluster"] = KMeans(n_clusters=optimal_k, init="k-means++", n_init=20, random_state=42)\
        .fit_predict(df_scaled[features_to_scale])
    df["Cluster"] = df_scaled["Cluster"]

    # Calculate cluster means for ranking
    cluster_means = df_scaled.groupby("Cluster")[features_to_scale].mean()
    cluster_means["score"] = (
        cluster_means["income"] * 0.1 +
        cluster_means["balance"] * 0.1 +
        cluster_means["debt"] * (-0.05) +  # Negative weight for financial distress
        cluster_means["customer_lifetime_value"] * 0.15 +  # CLV predicts revenue
        cluster_means["days_from_last_transaction"] * (-0.20) +  # Penalty for inactivity
        cluster_means["avg_transaction_amt"] * 0.20 +  # High-value customers spend more
        cluster_means["digital_engagement_score"] * 0.20 +  # More engagement means higher retention
        cluster_means["total_products_owned"] * 0.20 +  # More products indicate a stronger relationship
        cluster_means["num_transactions"] * 0.20  # Frequent usage matters
    )

    # Rank clusters based on score (descending)
    sorted_clusters = cluster_means["score"].sort_values(ascending=False).index.tolist()

    # Map clusters to segments based on ranking
    dynamic_segment_mapping = {
        sorted_clusters[0]: "High-value",
        sorted_clusters[1]: "Budget-conscious",
        sorted_clusters[2]: "At risk / inactive customers"
    }
    df["segment"] = df["Cluster"].map(dynamic_segment_mapping)

    return df[['customer_id', 'segment']]

def update_segments(conn, segments_df):
    """
    Update customer segments in the database.

    Args:
        conn (psycopg2.connection): Database connection.
        segments_df (pd.DataFrame): DataFrame with customer_id and segment.
    """
    with conn.cursor() as cur:
        # Iterate over each row and update the segment
        for _, row in segments_df.iterrows():
            cur.execute("""
                UPDATE customer_segments
                SET segment = %s
                WHERE customer_id = %s
            """, (row['segment'], row['customer_id']))
            print(f"Updated segments for cid = {row['customer_id']} to {row['segment']}!")
        conn.commit()

def process_transactions_batch(batch):
    """
    Process a mini batch of transactions: insert transactions, update customer metrics,
    recalculate clusters, and update customer segments.

    Args:
        batch (list): List of transaction dictionaries.
    """
    print(f"Processing batch of {len(batch)} transactions.")
    
    # Acquire a connection from the pool
    conn = conn_pool.getconn()
    cur = conn.cursor()

    # Batch insert query for transactions
    query = """
        INSERT INTO live_transaction_data (transaction_id, customer_id, transaction_amt, transaction_type, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = [
        (t['transaction_id'], t['customer_id'], t['transaction_amt'], 
         t['transaction_type'], datetime.fromisoformat(t['transaction_date']))
        for t in batch
    ]
    cur.executemany(query, data)
    conn.commit()

    # Batch update query for average transaction amount per customer
    query = """
        UPDATE customer_segments
        SET avg_transaction_amt = (
            SELECT AVG(transaction_amt::NUMERIC)
            FROM live_transaction_data
            WHERE customer_id = %s
        ) 
        WHERE customer_id = %s
    """
    cids = [(t['customer_id'], t['customer_id']) for t in batch]
    cur.executemany(query, cids)
    conn.commit()

    print(f'Updated avg_transaction_amt for {cids}!')

    # Recalculate clusters and update segments
    curr_customer_df = fetch_customer_data(conn)
    segments_df = recalculate_clusters(curr_customer_df)
    update_segments(conn, segments_df)

    # Close the cursor and return the connection to the pool
    cur.close()
    conn_pool.putconn(conn)

def consume_transactions_real_time():
    """
    Consume transactions from Kafka in real-time using micro-batching.
    A batch is processed either when the maximum batch size is reached or when the time window expires.
    """
    batch = []
    last_received = time.time()
    
    for message in consumer:
        transaction = message.value
        batch.append(transaction)
        
        # Process the batch if the batch size or time window condition is met
        if len(batch) >= MAX_BATCH_SIZE or (time.time() - last_received) >= MICRO_BATCH_WINDOW:
            process_transactions_batch(batch)
            batch = []  # Reset the batch after processing
            last_received = time.time()  # Reset the timer

def main():
    """
    Entry point for consuming transactions from Kafka.
    """
    consume_transactions_real_time()

if __name__ == '__main__':
    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        'customer_data',  # Kafka topic name
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=True,
        auto_offset_reset='earliest'
    )

    # Initialize connection pool for PostgreSQL
    conn_pool = pool.SimpleConnectionPool(
        1, 10, host=DB_NAME, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

    main()