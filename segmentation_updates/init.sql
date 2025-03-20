CREATE TABLE IF NOT EXISTS customer_segments (
    customer_id INT PRIMARY KEY,
    income MONEY,
    balance  MONEY,
    customer_lifetime_value FLOAT,
    debt MONEY,
    tenure INT,
    credit_default INT,
    days_from_last_transaction INT,
    avg_transaction_amt MONEY,
    loan_repayment_time INT,
    total_products_owned INT,
    has_loan INT,
    segment VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
);


CREATE TABLE IF NOT EXISTS live_transaction_data (
    transaction_id INT PRIMARY KEY,
    customer_id INT,
    transaction_amt MONEY,
    transaction_type VARCHAR(50),
    transaction_date TIMESTAMP,
)
