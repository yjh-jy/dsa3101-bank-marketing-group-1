import psycopg2
import os

#Obtain absolute reference path of import_date path
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_file_path_test = os.path.join(script_dir, '..', 'data', 'raw', 'test.csv')
csv_file_path_train = os.path.join(script_dir, '..', 'data', 'raw', 'train.csv')

DB_NAME = "postgres"
DB_USER = "postgres.gbcyjymnpmjvgjebbamb"
DB_PASSWORD = "dsa3101project"
DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com" 
DB_PORT = "6543"       
DB_POOLMODE: "transaction"

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASSWORD, 
    host=DB_HOST, 
    port=DB_PORT,
)

# Create a cursor
cur = conn.cursor()
print("Connected to PostgreSQL!")


#import test dataset

create_table_query = """
CREATE TABLE IF NOT EXISTS test_bank_dataset (
    age INT,
    job VARCHAR(50),
    marital VARCHAR(50),
    education VARCHAR(50),
    is_default VARCHAR(5),
    balance NUMERIC,
    housing VARCHAR(5),
    loan VARCHAR(5),
    contact VARCHAR(50),
    day INT,
    month VARCHAR(20),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome VARCHAR(50),
    y VARCHAR(5)
);
"""
cur.execute(create_table_query)


with open(csv_file_path_test, 'r', encoding='utf-8') as f:
    next(f)
    cur.copy_from(f, 'test_bank_dataset', sep=';', columns=("age","job","marital","education","is_default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","y"))

conn.commit()
print("test.csv data imported successfully!")

#import train.csv

create_table_query = """
CREATE TABLE IF NOT EXISTS train_bank_dataset (
    age INT,
    job VARCHAR(50),
    marital VARCHAR(50),
    education VARCHAR(50),
    is_default VARCHAR(5),
    balance NUMERIC,
    housing VARCHAR(5),
    loan VARCHAR(5),
    contact VARCHAR(50),
    day INT,
    month VARCHAR(20),
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    poutcome VARCHAR(50),
    y VARCHAR(5)
);
"""
cur.execute(create_table_query)


with open(csv_file_path_train, 'r', encoding='utf-8') as f:
    next(f)
    cur.copy_from(f, 'train_bank_dataset', sep=';', columns=("age","job","marital","education","is_default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","y"))

conn.commit()
print("train.csv data imported successfully!")


# Close connection when done
cur.close()
conn.close()
