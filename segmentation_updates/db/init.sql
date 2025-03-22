CREATE TABLE IF NOT EXISTS customer_segments (
    customer_id INT PRIMARY KEY,
    income FLOAT,
    balance FLOAT,
    customer_lifetime_value FLOAT,
    debt FLOAT,
    tenure INT,
    credit_default INT, 
    days_from_last_transaction FLOAT,
    avg_transaction_amt FLOAT,
    num_transactions FLOAT,
    digital_engagement_score FLOAT, 
    loan_repayment_time FLOAT,
    total_products_owned INT,
    has_loan INT,  
    segment VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS live_transaction_data (
    transaction_id INT PRIMARY KEY,
    customer_id INT,
    transaction_amt FLOAT,
    transaction_type VARCHAR(50),
    transaction_date TIMESTAMP
);

CREATE OR REPLACE FUNCTION update_last_updated_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_customer_segments_last_updated
BEFORE UPDATE ON customer_segments
FOR EACH ROW
EXECUTE FUNCTION update_last_updated_column();

COPY customer_segments (
    customer_id, income, balance, customer_lifetime_value, debt, tenure, 
    credit_default, days_from_last_transaction, avg_transaction_amt, num_transactions, 
    digital_engagement_score, loan_repayment_time, total_products_owned, 
    has_loan, segment
)
FROM '/csv_files/customer_segments_initial_data.csv.csv'  
DELIMITER ',' 
CSV HEADER;  -- Indicates that the first row is a header row