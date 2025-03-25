# Campaign-Level EDA
'''
This notebook analyses campaign characteristics in relation to customer engagement outcomes, 
focusing on potential drivers like campaign type, impressions, and click-through rate.
'''

import pandas as pd
import eda_functions as eda
from load_data import load_campaign_data
from feature_engineering import prepare_campaign_features
from data_quality import print_null_summary, print_shape_and_preview

# Load data
engagement_details, campaigns = load_campaign_data()
merged = engagement_details.merge(campaigns, on='campaign_id', how='left')

# Initial null check
print_null_summary(merged, "merged")
print_shape_and_preview(merged, "merged")

# Missing correlation diagnosis
eda.check_missing_correlation(merged, "clicks", "channel_used")
eda.check_missing_correlation(merged, "clicks", "campaign_type")

# Feature engineering
campaign_grouped = prepare_campaign_features(merged)

# Summary statistics
print_null_summary(campaign_grouped, "campaign_grouped")
print_shape_and_preview(campaign_grouped, "campaign_grouped")
print("\nSummary statistics:\n", campaign_grouped.describe(include='all'))

# Plot distributions for numeric variables
eda.plot_numeric_distributions(df=campaign_grouped, prefix="campaign")

# Categorical value counts and numeric exclusions
categorical_cols = eda.get_categorical_columns(campaign_grouped)
for col in categorical_cols:
    print(f"\nValue counts for {col}:\n{campaign_grouped[col].value_counts()}")

# Relationship analysis
eda.get_violin_plots_by_engagement_bin(campaign_grouped, target_col="engagement_rate")

numeric_cols = eda.get_numerical_columns(campaign_grouped)
print("\nCorrelation Matrix:\n", campaign_grouped[numeric_cols].corr())

eda.get_barplot(campaign_grouped, target_col="engagement_rate")
campaign_grouped["engagement_bin"] = pd.qcut(campaign_grouped["engagement_rate"], q=3, labels=["Low", "Medium", "High"])
chi2_results = eda.get_chi_square(campaign_grouped, "engagement_bin")
print("\nChi-Square Test Results:\n", chi2_results)