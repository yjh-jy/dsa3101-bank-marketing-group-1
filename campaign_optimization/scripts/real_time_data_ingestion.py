# main.py or any other file
from campaign_optimization import campaign_optimizer

# Use the optimizer
campaign = campaign_optimizer.select_campaign("Low Income", "25-34", "Email")
print(f"Selected Campaign: {campaign}")
