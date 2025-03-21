import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
#Obtain absolute reference path of import_date path
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_file_path_test = os.path.join(script_dir, '..', 'raw', 'test.csv')
csv_file_path_train = os.path.join(script_dir, '..', 'raw', 'bank_full.csv')


DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')  


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

#import bank_full.csv

create_table_query = """
CREATE TABLE IF NOT EXISTS bank_full_dataset (
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
    cur.copy_from(f, 'bank_full_dataset', sep=';', columns=("age","job","marital","education","is_default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","y"))

conn.commit()
print("bank_full.csv data uploaded to Supabase PosgresDB successfully!")


# Close connection when done
cur.close()
conn.close()




