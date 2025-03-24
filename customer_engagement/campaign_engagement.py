# Campaign-Level EDA
'''
This notebook analyses campaign characteristics in relation to customer engagement outcomes, 
focusing on potential drivers like campaign type, impressions, and click-through rate.
'''

# Load packages
import pandas as pd
import eda_functions as eda

# Load datasets
engagement_details = pd.read_csv("../data/processed/engagement_details.csv")
campaigns = pd.read_csv("../data/processed/campaigns.csv")

# Merge and check nulls
merged = engagement_details.merge(campaigns, on='campaign_id', how='left')
print(f"Null counts per column: \n {merged.isnull().sum()}")
print(f"\nShape of digital_usage: {merged.shape}")
print(f"\nFirst few rows of digital_usage:\n{merged.head()}")

# Check if nulls in `clicks` column is due to type of campaign or channel used (i.e. one that doesn't use clicks like the telephone)
clicks_missing_by_channel = eda.check_missing_correlation(merged, "clicks", "channel_used")
clicks_missing_by_type = eda.check_missing_correlation(merged, "clicks", "campaign_type")
# Conclusion from results: Nulls in `clicks` column is due to type of campaign/channel used, and not random
# Solution: Impute with 0

# Drop `duration` and impute missing `clicks` with 0
merged = merged.drop(columns="duration")
merged["clicks"] = merged["clicks"].fillna(0)

# Feature engineering

# Map month to quarter
month_to_quarter = {
    "January": "Q1", "February": "Q1", "March": "Q1",
    "April": "Q2", "May": "Q2", "June": "Q2",
    "July": "Q3", "August": "Q3", "September": "Q3",
    "October": "Q4", "November": "Q4", "December": "Q4"
}
merged["quarter"] = merged["month"].map(month_to_quarter)

# Aggregate to campaign_id level
campaign_grouped = (
    merged.groupby(["campaign_id", "channel_used"]).agg(
        num_targeted=("engagement_id", "count"),
        num_engaged=("has_engaged", "sum"),
        impressions=("impressions", "mean"),
        clicks=("clicks", "mean"),
        campaign_duration=("campaign_duration", "mean"),
        campaign_language=("campaign_language", "first"),
        target_audience=("target_audience", "first"),
        campaign_type=("campaign_type", "first"),
        quarter=("quarter", "first")
    ).reset_index()
)

campaign_grouped["engagement_rate"] = ( campaign_grouped["num_engaged"] / campaign_grouped["num_targeted"])
campaign_grouped["click_through_rate"] = ( campaign_grouped["clicks"] / campaign_grouped["impressions"])
campaign_grouped["impressions_per_day"] = ( campaign_grouped["impressions"] / campaign_grouped["campaign_duration"])
campaign_grouped["targets_per_day"] = ( campaign_grouped["num_targeted"] / campaign_grouped["campaign_duration"])
campaign_grouped["clicks_per_day"] = ( campaign_grouped["clicks"] / campaign_grouped["campaign_duration"])

# Drop extra columns
campaign_grouped = campaign_grouped.drop(columns=["campaign_id", "num_engaged", "num_targeted"])

# Summary statistics
campaign_grouped.describe(include='all')

# Plot distributions of campaign_grouped's numeric features
eda.plot_numeric_distributions(df=campaign_grouped, prefix="campaign")

# Value counts for campaign_grouped's categorical features

# Get object (str) columns
categorical_cols = campaign_grouped.select_dtypes(include="object").columns.tolist()
# Add numeric columns with <=5 unique values (treat as categorical)
categorical_cols += [col for col in campaign_grouped.columns
                     if campaign_grouped[col].dropna().nunique() <= 5 and
                     campaign_grouped[col].dtype in ["int64", "float64"] and col != "engagement_rate"]
for col in categorical_cols:
    print(f"\nValue counts for {col}:")
    print(campaign_grouped[col].value_counts())

# Relationship Analysis with `engagement_rate`

# 1. Violin plots for numeric features by engagement rate bin
eda.get_violin_plots_by_engagement_bin(campaign_grouped, target_col="engagement_rate")

# 2. Correlation matrix
numeric_cols = campaign_grouped.select_dtypes(include=["number"]).columns.difference(categorical_cols)
correlation_matrix = campaign_grouped[numeric_cols].corr()
correlation_matrix

# 3. Bar plots for engagement rate by categorical features
eda.get_barplot(campaign_grouped, target_col="engagement_rate")

# 4. Chi-square test for categorical features vs. binned engagement rate
campaign_grouped["engagement_bin"] = pd.qcut(campaign_grouped["engagement_rate"], q=3, labels=["Low", "Medium", "High"])
chi2_results = eda.get_chi_square(campaign_grouped, "engagement_bin")
print("\nChi-Square Test Results:\n", chi2_results)