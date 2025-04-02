import subprocess
import argparse
import os
import sys
import pandas as pd
from scipy.stats import mode

"""
Script gives a campaign suggestion based on a chosen customer segment

Parameters:
INCOME_LEVEL: Choose from ['Low Income', 'Medium Income', 'High Income']
AGE_RANGE: Choose from ['18-24', '25-34', '35-44', '45-54', '55+']
MEDIA_TYPE: Choose from ['Google Ads', 'Telephone', 'Website', 'Email', 'TikTok', 'Instagram', 'Landline']

Run in terminal:
docker exec -it campaign_optimization python campaign_suggestion.py "{INCOME_LEVEL}" "{AGE_RANGE}" "{MEDIA_TYPE}"

Returns: Optimal Campaign ID and its corresponding details
"""

# Ensure the /scripts directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "scripts"))

# Import campaign_optimizer from campaign_optimization
from campaign_optimization import campaign_optimizer

campaigns = pd.read_csv("/app/data/processed/campaigns.csv")

INCOME_LEVEL = "High Income" # Choose from ['Low Income', 'Medium Income', 'High Income']
AGE_RANGE = "18-24" # Choose from ['18-24', '25-34', '35-44', '45-54', '55+']
MEDIA_TYPE = "Google Ads" # Choose from ['Google Ads', 'Telephone', 'Website', 'Email', 'TikTok', 'Instagram', 'Landline']

def recommend_campaign(income_level, age_range, media_type):
    campaign_selection = []
    for _ in range(200):
        campaign_selection.append(campaign_optimizer.select_campaign(income_level, age_range, media_type))

    most_common_campaign = mode(campaign_selection, keepdims=False).mode  # Get the mode
    print("Most Selected Campaign:", most_common_campaign)  
    campaign_details = campaigns[campaigns["campaign_id"] == most_common_campaign]
    print(campaign_details)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recommend a marketing campaign based on customer attributes.")
    parser.add_argument("income_level", choices=["Low Income", "Medium Income", "High Income"], help="Customer income level")
    parser.add_argument("age_range", choices=["18-24", "25-34", "35-44", "45-54", "55+"], help="Customer age range")
    parser.add_argument("media_type", choices=["Google Ads", "Telephone", "Website", "Email", "TikTok", "Instagram", "Landline"], help="Marketing media type")

    args = parser.parse_args()

    recommend_campaign(args.income_level, args.age_range, args.media_type)




