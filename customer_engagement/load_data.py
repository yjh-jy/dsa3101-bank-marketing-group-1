import pandas as pd

def load_customer_data():
    '''
    Loads csv files for customer-level engagement analysis
    '''
    engagement_details = pd.read_csv("../data/processed/engagement_details.csv")
    customers = pd.read_csv("../data/processed/customer.csv")
    digital_usage = pd.read_csv("../data/processed/digital_usage.csv")
    products_owned = pd.read_csv("../data/processed/products_owned.csv")
    transactions = pd.read_csv("../data/processed/transactions.csv")
    return engagement_details, customers, digital_usage, products_owned, transactions

def load_campaign_data():
    '''
    Loads csv files for campaign-level engagement analysis
    '''
    engagement_details = pd.read_csv("../data/processed/engagement_details.csv")
    campaigns = pd.read_csv("../data/processed/campaigns.csv")
    return engagement_details, campaigns