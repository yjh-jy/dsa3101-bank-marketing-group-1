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
import os
from datetime import datetime

from sklearn.discriminant_analysis import StandardScaler
from sklearn.preprocessing import RobustScaler
from scipy.stats.mstats import winsorize

load_dotenv()

KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
DB_NAME="postgres"
DB_USER="postgres"
DB_PASSWORD="dsa3101project"
DB_HOST="postgres" 
DB_PORT="5433"

# Micro-batching parameters
MICRO_BATCH_WINDOW = 0.1  # 100ms time window (for example)
MAX_BATCH_SIZE = 10       # Max transactions to accumulate before processing

# Fetch customer data for clustering
def fetch_customer_data(conn):
    query = """
        SELECT customer_id, income, balance, customer_lifetime_value, debt, tenure, credit_default, days_from_last_transaction ,
        avg_transaction_amt ,
        num_transactions ,
        digital_engagement_score , 
        loan_repayment_time ,
        total_products_owned ,
        has_loan 
        FROM customer_segments
    """
    df = pd.read_sql(query, conn)
    return df

# Perform KMeans clustering and update segments
def recalculate_clusters(df):
    features_to_scale = ["income", "balance", "debt", "customer_lifetime_value", 
                    "days_from_last_transaction", "avg_transaction_amt", 
                    "digital_engagement_score", "total_products_owned", 
                    "loan_repayment_time", "num_transactions"]
    
    robust_features = ["income", "balance", "debt", "customer_lifetime_value",  "avg_transaction_amt"]
    for col in robust_features:
        df[col] = pd.Series(winsorize(df[col].to_numpy(), limits=[0.05, 0.05]))

    # Features that need Standard scaling (normally distributed)
    standard_features = ["days_from_last_transaction",  "digital_engagement_score", "total_products_owned", "loan_repayment_time", "num_transactions"]

    # Apply RobustScaler
    scalerrobust =  RobustScaler()
    df_scaled = df.copy()
    df_scaled[robust_features] = scalerrobust.fit_transform(df[robust_features])

    # Apply StandardScaler
    scaler_standard = StandardScaler()
    df_scaled[standard_features] = scaler_standard.fit_transform(df[standard_features])

    ## K-MEANS CLUSTERING
    optimal_k = 3
    df_scaled["Cluster"] = KMeans(n_clusters= optimal_k,  init="k-means++", n_init=20, random_state=42).fit_predict(df_scaled[features_to_scale])
    df["Cluster"] = df_scaled["Cluster"]

    ### Get information about each cluster
    cluster_means = df_scaled.groupby("Cluster")[features_to_scale].mean()

    cluster_means["score"] = (
        cluster_means["income"] * 0.1 + 
        cluster_means["balance"] * 0.1 + 
        cluster_means["debt"] * (-0.05) +  # Negative weight for financial distress
        cluster_means["customer_lifetime_value"] * 0.15 +  # Increased because CLV predicts revenue
        cluster_means["days_from_last_transaction"] * (-0.20) +  # Increased penalty for inactivity
        cluster_means["avg_transaction_amt"] * 0.20 +  # High-value customers spend more per transaction
        cluster_means["digital_engagement_score"] * 0.20 +  # More engagement means higher retention
        cluster_means["total_products_owned"] * 0.20 +  # Owning more products = stronger banking relationship
        cluster_means["num_transactions"] * 0.20  # Higher impact because frequent usage matters
    )

    # Step 2: Rank Clusters Based on Score (Descending)
    sorted_clusters = cluster_means["score"].sort_values(ascending=False).index.tolist()

    # Step 3: Assign Segments Based on Rank
    dynamic_segment_mapping = {
        sorted_clusters[0]: "High-value",
        sorted_clusters[1]: "Budget-conscious",
        sorted_clusters[2]: "At risk / inactive customers"
    }
    df["segment"] = df["Cluster"].map(dynamic_segment_mapping)

    return df[['customer_id', 'segment']]

# Update customer segments in the database
def update_segments(conn, segments_df):
    with conn.cursor() as cur:
        for _, row in segments_df.iterrows():
            cur.execute("""
                UPDATE customer_segments
                SET segment = %s
                WHERE customer_id = %s
            """, (row['segment'], row['customer_id']))

            print(f"Updated segments for cid = {row['customer_id']} to {row['segment']}!")
        conn.commit()

# Process the transactions in mini batches
def process_transactions_batch(batch):
    """Process a mini batch of transactions."""
    print(f"Processing batch of {len(batch)} transactions.")
    # Get a connection from the pool
    conn = conn_pool.getconn()
    cur = conn.cursor()

    # Prepare a batch insert query
    query = """
        INSERT INTO live_transaction_data (transaction_id, customer_id, transaction_amt, transaction_type, transaction_date)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    # Prepare the data
    data = [(t['transaction_id'], t['customer_id'], t['transaction_amt'], t['transaction_type'], datetime.fromisoformat(t['transaction_date'])) for t in batch]
    
    # Insert the batch of transactions
    cur.executemany(query, data)
    conn.commit()

    query ="""
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

    curr_customer_df = fetch_customer_data(conn)
    segments_df = recalculate_clusters(curr_customer_df)
    update_segments(conn, segments_df)

    # Close the cursor and return the connection to the pool
    cur.close()
    conn_pool.putconn(conn)

def consume_transactions_real_time():
    """Consume transactions in real-time with micro-batching."""
    batch = []
    last_received = time.time()
    
    for message in consumer:
        transaction = message.value
        batch.append(transaction)
        
        # If the batch size or time window exceeds limits, process the batch
        if len(batch) >= MAX_BATCH_SIZE or (time.time() - last_received) >= MICRO_BATCH_WINDOW:
            process_transactions_batch(batch)
            batch = []  # Reset the batch
            last_received = time.time()  # Reset the timer for the next batch

def main():
    consume_transactions_real_time()

if __name__ == '__main__':
    # Kafka Consumer
    consumer = KafkaConsumer(
        'customer_data',  # Kafka topic name
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        enable_auto_commit=True,
        auto_offset_reset='earliest'
    )

    # Connection pool
    conn_pool = pool.SimpleConnectionPool(
    1, 10, host=DB_NAME, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )

    main()
