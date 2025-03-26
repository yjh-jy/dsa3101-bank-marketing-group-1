import pandas as pd
import numpy as np
import random
import psycopg2
from scipy.stats import mode

# Thompson Sampling Class
class CampaignOptimizer:
    def __init__(self, alpha, beta):
        self.alpha = alpha  # Successes
        self.beta = beta   # Failures

    def select_campaign(self, income_level, target_audience, channel_type):
        available_campaigns = [k[0] for k in self.alpha.keys() if k[1] == income_level and k[2] == target_audience and k[3] == channel_type]
        samples = {}

        for campaign in available_campaigns:
            key = (campaign, income_level, target_audience, channel_type)
            alpha_val = self.alpha.get(key,1)
            beta_val = self.beta.get(key,1)
            samples[campaign] = np.random.beta(alpha_val, beta_val)
        
        if not samples:
            return None #No suitable campaign
         
        return max(samples, key=samples.get) #Choose campaign with highest distribution


    def update_campaign(self, campaign, income_level, target_audience, channel_type, success):
        """Updates the Bayesian model with new engagement data"""
        key = (campaign, income_level, target_audience, channel_type)

        if key not in self.alpha:            
            prior_strength = 2  # Adjust this based on dataset size
            prior_alpha = global_mean_engagement * prior_strength
            prior_beta = (1 - global_mean_engagement) * prior_strength
            
            alpha[key] = row["successful_engagements"] + prior_alpha  
            beta[key] = (row["total_attempts"] - row["successful_engagements"]) + prior_beta  

        if success:
            self.alpha[key] += 3
        else:
            self.beta[key] += 3

#Read campaigns data
campaigns = pd.read_csv("/app/data/processed/campaigns.csv")

# Connect to PostgreSQL

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "dsa3101project"
DB_HOST = "postgres"
DB_PORT = "5432"

conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

query = """
SELECT campaign_id, income_category, target_audience, channel_used, has_engaged
FROM Engagements;
"""

engagements = pd.read_sql(query,conn)

cur.close()
conn.close()

# Group by campaign and calculate engagement success rate
campaign_stats = engagements.groupby(["campaign_id", "income_category", "target_audience", "channel_used"]).agg(
    total_attempts=("has_engaged", "count"),
    successful_engagements=("has_engaged", "sum")
).reset_index()

# Calculate engagement rate
campaign_stats["engagement_rate"] = campaign_stats["successful_engagements"] / campaign_stats["total_attempts"]

# Create alpha and beta values
alpha = {}
beta = {}

global_mean_engagement = campaign_stats["engagement_rate"].mean()

for index, row in campaign_stats.iterrows():
    key = (row["campaign_id"], row["income_category"], row["target_audience"], row["channel_used"])
    
    prior_strength = 2  # Adjust this based on dataset size
    prior_alpha = global_mean_engagement * prior_strength
    prior_beta = (1 - global_mean_engagement) * prior_strength
    
    alpha[key] = row["successful_engagements"] + prior_alpha  
    beta[key] = (row["total_attempts"] - row["successful_engagements"]) + prior_beta  

# Initialize campaign optimizer
campaign_optimizer = CampaignOptimizer(alpha, beta)


def simulate_engagement(campaign_id, income_category, target_audience, channel_used):
    """Simulate customer engagement based on past data"""
    engagement_prob = campaign_stats.loc[(campaign_stats["campaign_id"] == campaign_id) & (campaign_stats["income_category"] == income_category) 
                                         & (campaign_stats["target_audience"] == target_audience) & (campaign_stats["channel_used"] == channel_used), 
                                         "engagement_rate"].values[0]
    return random.random() < engagement_prob  # Simulate success/failure

# Update initial alpha-beta values with prior data
campaign_stats_concise = campaign_stats[["campaign_id", "income_category", "target_audience", "channel_used", "engagement_rate"]]


for _ in range(2):
    for index, row in campaign_stats_concise.iterrows():
        campaign_id = row["campaign_id"]
        income_category = row["income_category"]
        target_audience = row["target_audience"]
        channel_used = row["channel_used"]
        engagement_rate = row["engagement_rate"]
        engagement_results = simulate_engagement(campaign_id, income_category, target_audience, channel_used)
        campaign_optimizer.update_campaign(campaign_id, income_category, target_audience, channel_used, engagement_results)


campaign_selection = []
for _ in range(200):
    campaign_selection.append(campaign_optimizer.select_campaign("Low Income", "25-34", "Email"))
most_common_campaign = mode(lol, keepdims=False).mode  # Get the mode
print("Most Selected Campaign:", most_common_campaign)    


campaign_details = campaigns[campaigns["campaign_id"] == most_common_campaign]
print(campaign_details)