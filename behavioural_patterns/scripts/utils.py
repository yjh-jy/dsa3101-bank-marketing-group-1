# Importing packages
import os
import pandas as pd
import numpy as np

def load_data():
    """
    Load all required datasets.
    
    Returns:
        Tuple of DataFrames: customers, digital_usage, loans, products, transactions, segments.
    """
    # Reading in datasets
    project_root = os.getcwd()  
    data_path = os.path.join(project_root, "data", "processed")
    customers = pd.read_csv(os.path.join(data_path, "customer.csv"))
    digital_usage = pd.read_csv(os.path.join(data_path, "digital_usage.csv"))
    loans = pd.read_csv(os.path.join(data_path, "loans.csv"))
    products = pd.read_csv(os.path.join(data_path, "products_owned.csv"))
    transactions = pd.read_csv(os.path.join(data_path, "transactions.csv"))
    segments = pd.read_csv(os.path.join(data_path, "..", "..", "customer_segmentation", "customer_segments.csv"))
    return customers, digital_usage, loans, products, transactions, segments

def categorize_loan_purpose(purpose):
    """
    Categorize loan purpose into broader categories.
    """
    # If the loan purpose is debt_consolidation, assign Debt Management
    if purpose == 'debt_consolidation':
        return 'Debt Management'
    # If the loan purpose is credit_card, assign Credit Product
    elif purpose == 'credit_card':
        return 'Credit Product'
    # If the loan purpose is housing-related, major_purchase, or car, assign Asset Acquisition
    elif purpose in ['housing-related', 'major_purchase', 'car']:
        return 'Asset Acquisition'
    # If the loan purpose is small_business or educational, assign Business & Education
    elif purpose in ['small_business', 'educational']:
        return 'Business & Education'
    # If the loan purpose is wedding, vacation, or medical, assign Lifestyle & Personal
    elif purpose in ['wedding', 'vacation', 'medical']:
        return 'Lifestyle & Personal'
    else:
        # For all other purposes, assign Miscellaneous
        return 'Miscellaneous'

def classify_money_flow(tx_type):
    """
    Classify a transaction as 'Money In' or 'Money Out'.
    """
    # If the transaction type is Credit or Deposit, return Money In; otherwise, Money Out.
    if tx_type in ['Credit', 'Deposit']:
        return 'Money In'
    else:
        return 'Money Out'

def prepare_data(customers, digital_usage, loans, products, transactions, segments):
    """
    Prepare and merge datasets with necessary transformations.
    
    Returns:
        df: The merged and transformed DataFrame.
    """
    # Merging segments and customers datasets
    df = pd.merge(segments, customers, on='customer_id')
    
    # Converting 'job', 'marital', and 'education' columns to category data type
    categorical_columns = ['job', 'marital', 'education']
    for col in categorical_columns:
        df[col] = df[col].astype('category')
    
    # Creating 'nps_category' column that segments responses into promoters, passives, and detractors
    nps_bins = [-float('inf'), 6, 8, 10]
    nps_labels = ['detractor', 'passive', 'promoter']
    df['nps_category'] = pd.cut(df['nps'], bins=nps_bins, labels=nps_labels)
    
    # Dropping the original 'nps' column
    df.drop(['nps'], axis=1, inplace=True)
    
    # Applying log transformation to 'balance', 'debt', and 'income' to scale and stabilize the values
    df['log_balance'] = np.sign(df['balance']) * np.log1p(np.abs(df['balance']))
    df['log_debt'] = np.log1p(df['debt'])
    df['log_income'] = np.log1p(df['income'])
    
    # Creating 'debt-to-income' ratio and 'balance-to-debt' ratio columns
    df['debt_to_income'] = df['log_debt'] / df['log_income']
    df['balance_to_debt'] = df['log_balance'] / df['log_debt']
    
    # Converting 'due_date' and 'paid_off_date' columns to datetime format in the loans dataset
    loans['due_date'] = pd.to_datetime(loans['due_date'])
    loans['paid_off_date'] = pd.to_datetime(loans['paid_off_date'])
    
    # Creating 'days_past_due' column
    loans['days_past_due'] = (loans['paid_off_date'] - loans['due_date']).dt.days
    loans['days_past_due'] = loans['days_past_due'].fillna(0)
    
    # Dropping the original 'due_date' and 'paid_off_date' columns
    loans.drop(['due_date', 'paid_off_date'], axis=1, inplace=True)
    
    # Categorize loan purposes into broader categories and create 'loan_category' column
    loans['loan_category'] = loans['loan_purpose'].apply(categorize_loan_purpose)
    
    # Converting 'transaction_type' column to category data type in transactions dataset
    transactions['transaction_type'] = transactions['transaction_type'].astype('category')
    
    # Extracting year-month-day from 'transaction_date' and converting to datetime format
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    transactions['transaction_date'] = transactions['transaction_date'].dt.date
    transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
    
    # Categorizing transactions as 'Money In' or 'Money Out', and creating 'money_flow' column
    transactions['money_flow'] = transactions['transaction_type'].apply(classify_money_flow)
    
    # Converting 'last_mobile_use' and 'last_web_use' columns to datetime format in digital_usage dataset
    digital_usage['last_mobile_use'] = pd.to_datetime(digital_usage['last_mobile_use'])
    digital_usage['last_web_use'] = pd.to_datetime(digital_usage['last_web_use'])
    
    # Creating 'mobile_web_ratio' column
    digital_usage['mobile_web_ratio'] = digital_usage['mobile_logins_wk'] / digital_usage['web_logins_wk']
    
    # Merging products, loans, transactions, and digital_usage datasets with df
    df = df.merge(products, on='customer_id')
    df = df.merge(loans, on='customer_id')
    df = df.merge(transactions, on='customer_id')
    df = df.merge(digital_usage, on='customer_id')
    
    return df