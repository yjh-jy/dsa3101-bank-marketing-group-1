import pandas as pd
import os

def load_data(data_path):
    """
    Load customer, campaign, and engagement detail data.

    Parameters:
    - data_path (str): Directory where the processed .csv files are stored.

    Returns:
    - Tuple of DataFrames: (customer_df, campaigns_df, engagement_df)
    """
    customer_df = pd.read_csv(os.path.join(data_path, "customer.csv"))
    campaigns_df = pd.read_csv(os.path.join(data_path, "campaigns.csv"))
    engagement_df = pd.read_csv(os.path.join(data_path, "engagement_details.csv"))
    return customer_df, campaigns_df, engagement_df
