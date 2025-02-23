import psycopg2
import os

#Obtain absolute reference path of import_date path
script_dir = os.path.dirname(os.path.abspath(__file__))

csv_file_path = os.path.join(script_dir, '..', 'data', 'raw', 'test.csv')
print(csv_file_path)

DB_NAME = "dsa3101"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost" 
DB_PORT = "5432"       

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASSWORD, 
    host=DB_HOST, 
    port=DB_PORT
)

# Create a cursor
cur = conn.cursor()
print("Connected to PostgreSQL!")

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



with open(csv_file_path, 'r', encoding='utf-8') as f:
    next(f)
    cur.copy_from(f, 'test_bank_dataset', sep=';', columns=("age","job","marital","education","is_default","balance","housing","loan","contact","day","month","duration","campaign","pdays","previous","poutcome","y"))

conn.commit()
print("test.csv data imported successfully!")


# Close connection when done
cur.close()
conn.close()
