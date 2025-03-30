import pandas as pd

def load_data():
    '''
    Load customer, campaign, and engagement detail data
    '''
    customer_df = pd.read_csv("../data/processed/customer.csv")
    campaigns_df = pd.read_csv("../data/processed/campaigns.csv")
    engagement_df = pd.read_csv("../data/processed/engagement_details.csv")
    return customer_df, campaigns_df, engagement_df