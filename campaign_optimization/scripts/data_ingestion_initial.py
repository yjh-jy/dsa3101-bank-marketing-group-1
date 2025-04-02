import pandas as pd
import numpy as np
import os
import psycopg2

"""
Script helps to digest initial dataset from csv into Engagements table in PostgreSQL
"""



# Kafka and database configurations
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'kafka:9092')
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "dsa3101project"
DB_HOST = "postgres"
DB_PORT = "5432"

print("Script Path:", os.path.abspath(__file__))
# Load Relevant Data
customers = pd.read_csv("../app/data/processed/customer.csv")
engagements = pd.read_csv("../app/data/processed/engagement_details.csv")
campaigns = pd.read_csv("../app/data/processed/campaigns.csv")

def categorize_income(income):
    if income < 3000:
        return "Low Income"
    elif 3000 <= income <= 6000:
        return "Medium Income"
    else:
        return "Hign Income"

customers["income_category"] = customers["income"].apply(categorize_income) 


# Merge Engagements with Campaigns
engagements = engagements.merge(campaigns, on="campaign_id")
engagements = engagements.merge(customers, on='customer_id') 
engagements = engagements[["campaign_id", "income_category", "target_audience", "channel_used", "has_engaged"]]


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()


# Insert data into PostgreSQL
for _, row in engagements.iterrows():
    insert_query = """
    INSERT INTO engagements (campaign_id, income_category, target_audience, channel_used, has_engaged)
    VALUES (%s, %s, %s, %s, %s);
    """  # Prevents duplicate primary key errors
    cur.execute(insert_query, tuple(row))

# Commit and close connection
conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")