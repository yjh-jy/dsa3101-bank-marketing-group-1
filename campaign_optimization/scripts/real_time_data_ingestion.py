from kafka import KafkaConsumer
import json
import os
from campaign_optimization import optimizer_instance

# Use the optimizer
campaign = campaign_optimizer.select_campaign("Low Income", "25-34", "Email")
print(f"Selected Campaign: {campaign}")
