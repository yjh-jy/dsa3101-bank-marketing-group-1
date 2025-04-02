import subprocess
import os
import sys
import pandas as pd
from scipy.stats import mode

# Ensure the /scripts directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import campaign_optimizer from campaign_optimization
from campaign_optimization import campaign_optimizer

campaigns = pd.read_csv("/app/data/processed/campaigns.csv")

INCOME_LEVEL = "Low Income" # Choose from ['Low Income', 'Medium Income', 'High Income']
AGE_RANGE = "25-34" # Choose from ['18-24', '25-34', '35-44', '45-54', '55+']
MEDIA_TYPE = "Email" # Choose from ['Google Ads', 'Telephone', 'Website', 'Email', 'TikTok', 'Instagram', 'Landline']

def recommend_campaign(income_level, age_range, media_type):
    campaign_selection = []
    for _ in range(200):
        campaign_selection.append(campaign_optimizer.select_campaign("Low Income", "25-34", "Email"))


    most_common_campaign = mode(campaign_selection, keepdims=False).mode  # Get the mode
    print("Most Selected Campaign:", most_common_campaign)    


    campaign_details = campaigns[campaigns["campaign_id"] == most_common_campaign]
    print(campaign_details)


recommend_campaign(INCOME_LEVEL, AGE_RANGE, MEDIA_TYPE)


