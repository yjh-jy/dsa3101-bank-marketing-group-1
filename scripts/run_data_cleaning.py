import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from io import StringIO
import numpy as np

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')  

conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASSWORD, 
    host=DB_HOST, 
    port=DB_PORT,
)
cur = conn.cursor()
cur.execute("SELECT * FROM train_bank_dataset;")

rows = cur.fetchall()
column_names = [desc[0] for desc in cur.description]

df = pd.DataFrame(rows, columns = column_names)

#is_default, housing, loan, y
#balance -> integer, month -> integer

#binary-encoding
binary_encoding = {
    'is_default': {'"no"': 0, '"yes"': 1},
    'housing': {'"no"': 0, '"yes"': 1},
    'loan': {'"no"': 0, '"yes"': 1},
    'y': {'"no"': 0, '"yes"': 1}
}

def apply_ordinal_encoding(df, encodings):
    for column, mapping in encodings.items():
        df[column] = df[column].map(mapping)
    return df

df_clean = apply_ordinal_encoding(df, binary_encoding)

#month-encoding
month_dict = {
    '"jan"':1,
    '"feb"':2,
    '"mar"':3,
    '"apr"':4,
    '"may"':5,
    '"jun"':6,
    '"jul"':7,
    '"aug"':8,
    '"sep"':9,
    '"oct"':10,
    '"nov"':11,
    '"dec"':12,
}

df_clean.month = df.month.apply(lambda x: month_dict[x])

#One-Hot Encoding for categorical data
df_clean = pd.get_dummies(df_clean, dtype=int, columns=['job', 'marital', 'education', 'contact', 'poutcome'])

#Change balance type from object to int
df_clean.balance = df.balance.fillna(0).astype(int)


#Upload to Database
create_table_query = """
CREATE TABLE IF NOT EXISTS bank_full_dataset_cleaned (
    age INT,
    job_admin INT,
    job_blue_collar INT,
    job_entrepreneur INT,
    job_housemaid INT,
    job_management INT,
    job_retired INT,
    job_self_employed INT,
    job_services INT,
    job_student INT,
    job_technician INT,
    job_unemployed INT,
    job_unknown INT,
    marital_divorced INT,
    marital_married INT,
    marital_single INT,
    education_primary INT,
    education_secondary INT,
    education_tertiary INT,
    education_unknown INT,
    contact_cellular INT,
    contact_telephone INT,
    contact_unknown INT,
    poutcome_failure INT,
    poutcome_other INT,
    poutcome_success INT,
    poutcome_unknown INT,
    is_default INT,
    balance NUMERIC,
    housing INT,
    loan INT,
    day INT,
    month INT,
    duration INT,
    campaign INT,
    pdays INT,
    previous INT,
    y INT
);
"""

cur.execute(create_table_query)

temp_csv_path = 'temp_data.csv'
csv_data = df_clean.to_csv(temp_csv_path, index=False, sep=';')

with open(temp_csv_path, 'r', encoding='utf-8') as csv_file:
    next(csv_file)
    cur.copy_from(csv_file, 'bank_full_dataset_cleaned', sep=';', 
                columns=["age", "job_admin", "job_blue_collar", "job_entrepreneur",
                        "job_housemaid", "job_management", "job_retired",
                        "job_self_employed", "job_services", "job_student",
                        "job_technician", "job_unemployed", "job_unknown",
                        "marital_divorced", "marital_married", "marital_single",
                        "education_primary", "education_secondary", "education_tertiary",
                        "education_unknown", "contact_cellular", "contact_telephone",
                        "contact_unknown", "poutcome_failure", "poutcome_other",
                        "poutcome_success", "poutcome_unknown", "is_default", "balance", 
                        "housing", "loan", "day", "month", "duration", "campaign", 
                        "pdays", "previous", "y"])
    
conn.commit()
print("bank_full_dataset_cleaned success!")