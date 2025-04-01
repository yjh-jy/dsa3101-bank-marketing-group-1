# Importing packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_theme(style="whitegrid")

# Global constants
VISUALS_PATH = "campaign_impact_analysis/insights/visuals"
os.makedirs(VISUALS_PATH, exist_ok=True)

def load_data():
    """
    Load and prepare all required datasets.
    
    Returns:
        tuple: Tuple containing all loaded dataframes
    """
    campaigns_df = pd.read_csv("data/processed/campaigns.csv")
    customer_df = pd.read_csv("data/processed/customer.csv")
    digital_usage_df = pd.read_csv("data/processed/digital_usage.csv")
    engagement_details_df = pd.read_csv("data/processed/engagement_details.csv")
    loans_df = pd.read_csv("data/processed/loans.csv")
    products_owned_df = pd.read_csv("data/processed/products_owned.csv")
    transactions_df = pd.read_csv("data/processed/transactions.csv")
    segmentation_df = pd.read_csv("customer_segmentation/customer_segments.csv")
    
    print('Loaded Data Shapes:')
    print('Campaign:', campaigns_df.shape)
    print('Customer:', customer_df.shape)
    print('DigitalUsage:', digital_usage_df.shape)
    print('EngagementDetail:', engagement_details_df.shape)
    print('Loan:', loans_df.shape)
    print('ProductsOwned:', products_owned_df.shape)
    print('Transaction:', transactions_df.shape)
    
    return (campaigns_df, customer_df, digital_usage_df, engagement_details_df, 
            loans_df, products_owned_df, transactions_df, segmentation_df)

def analyze_campaign_target_audience(campaign_customers_df):
    """
    Analyze and visualize customer engagement by campaign type and target audience.
    
    Args:
        campaign_customers_df (DataFrame): Combined dataframe with campaign and customer data
    """
    g = sns.FacetGrid(campaign_customers_df, col="campaign_type", col_wrap=3, height=4, sharex=False)
    g.map_dataframe(sns.countplot, x='target_audience', order=sorted(campaign_customers_df['target_audience'].unique()))

    # Annotate each bar with the count
    for ax in g.axes.flat:
        for bar in ax.patches:
            height = bar.get_height()
            ax.annotate(f'{int(height)}', 
                        xy=(bar.get_x() + bar.get_width() / 2, height), 
                        xytext=(0, 4),  # Offset text slightly above the bar
                        textcoords="offset points", 
                        ha='center', va='center', fontsize=9)

    g.set_axis_labels('Age Group', 'Number of Customers Engaged')
    g.set_titles(col_template='{col_name}')
    g.figure.suptitle('Customer Engagement by Campaign Type and Target Audience', y=1.05)
    plt.savefig(f"{VISUALS_PATH}/campaign_target_audience_by_type.png", bbox_inches="tight", dpi=300)
    plt.close()

def is_age_in_target(row):
    """
    Check if customer age is within the target audience range.
    
    Args:
        row (Series): DataFrame row containing 'age' and 'target_audience'
        
    Returns:
        bool: True if age is within target range, False otherwise
    """
    age = row['age']
    target = row['target_audience']
    if target == '18-24':
        return 18 <= age <= 24
    elif target == '25-34':
        return 25 <= age <= 34
    elif target == '35-44':
        return 35 <= age <= 44
    elif target == '45-54':
        return 45 <= age <= 54
    elif target == '55+':
        return age >= 55
    else:
        return False

def analyze_age_mismatch(campaign_customers_df):
    """
    Analyze the mismatch between campaign target audience and actual customer ages.
    
    Args:
        campaign_customers_df (DataFrame): Combined dataframe with campaign and customer data
    """
    # Apply the function to create a new column
    campaign_customers_df['age_in_target'] = campaign_customers_df.apply(is_age_in_target, axis=1)

    # Group by campaign_id and count the number of rows where age_in_target is False
    age_mismatch_rate = campaign_customers_df.groupby('campaign_id').apply(lambda x: (~x['age_in_target']).mean(), include_groups=False) * 100

    print("Percentage mismatch between campaign target audience and actual engaged customer age:")
    print(age_mismatch_rate)

def analyze_engagement_rates(engagement_details_df, campaigns_df):
    """
    Analyze overall engagement rate and engagement rate by channel.
    
    Args:
        engagement_details_df (DataFrame): Engagement details data
        campaigns_df (DataFrame): Campaign data
    """
    # Engagement rate overall
    engagement_rate = engagement_details_df["has_engaged"].mean() * 100
    print(f"Overall Engagement Rate: {engagement_rate:.2f}%")

    # Engagement rate by communication channel used
    engagement_campaign_df = engagement_details_df.merge(campaigns_df, on="campaign_id")
    engagement_by_channel = engagement_campaign_df.groupby("channel_used")["has_engaged"].mean().sort_values() * 100

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=engagement_by_channel.index, y=engagement_by_channel.values)
    plt.title("Engagement Rate by Channel")
    plt.xlabel("Channel Used")
    plt.ylabel("Engagement Rate (%)")

    # Annotate each bar with the number
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', 
                    xy=(bar.get_x() + bar.get_width() / 2, height), 
                    xytext=(0, 4),  # Offset text slightly above the bar
                    textcoords="offset points", 
                    ha='center', va='center', fontsize=9)

    plt.savefig(f"{VISUALS_PATH}/engagement_rate_by_channel.png", bbox_inches="tight", dpi=300)
    plt.close()

def analyze_monthly_engagement(campaign_customers_df):
    """
    Analyze engagement rate and campaign counts by month.
    
    Args:
        campaign_customers_df (DataFrame): Combined dataframe with campaign and customer data
    """
    campaign_customers_df["month"] = pd.Categorical(campaign_customers_df["month"], 
                                                   categories=["January", "February", "March", "April", 
                                                              "May", "June", "July", "August", "September", 
                                                              "October", "November", "December"], 
                                                   ordered=True)
    engagement_rate = campaign_customers_df.groupby("month", observed=True)["has_engaged"].mean() * 100
    campaign_counts = campaign_customers_df.groupby("month", observed=True)["campaign_id"].nunique().sort_index()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    engagement_rate.plot(kind='bar', ax=ax1, color='orange')
    ax1.set_title('Average Engagement Rate per Month')
    ax1.set_ylabel('Average Engagement Rate (%)')
    ax1.set_xlabel('Month')

    # Annotate bars in the first plot
    for bar in ax1.patches:
        height = bar.get_height()
        ax1.annotate(f'{height:.1f}%', 
                     xy=(bar.get_x() + bar.get_width() / 2, height), 
                     xytext=(0, 4),  # Offset text slightly above the bar
                     textcoords="offset points", 
                     ha='center', va='center', fontsize=9)

    campaign_counts.plot(kind='bar', ax=ax2, color='lightblue')
    ax2.set_title('Number of Unique Campaigns per Month')
    ax2.set_ylabel('Unique Campaigns')

    # Annotate bars in the second plot
    for bar in ax2.patches:
        height = bar.get_height()
        ax2.annotate(f'{int(height)}', 
                     xy=(bar.get_x() + bar.get_width() / 2, height), 
                     xytext=(0, 4),  # Offset text slightly above the bar
                     textcoords="offset points", 
                     ha='center', va='center', fontsize=9)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{VISUALS_PATH}/campaign_engagement_by_month.png", bbox_inches="tight", dpi=300)
    plt.close()

def analyze_engagement_conversion_correlation(engagement_details_df, campaigns_df):
    """
    Analyze the correlation between engagement rate and conversion rate.
    
    Args:
        engagement_details_df (DataFrame): Engagement details data
        campaigns_df (DataFrame): Campaign data
    """
    engagement_rate = engagement_details_df.groupby("campaign_id")["has_engaged"].mean() * 100
    df = campaigns_df.merge(engagement_rate, on="campaign_id")
    df["conversion_rate"] = df["conversion_rate"] * 100
    df["type"] = df["campaign_type"].apply(lambda x: "Digital" if x in ["Display Advertising", "Affiliate Marketing"] else "Traditional")
    correlation = df["conversion_rate"].corr(df["has_engaged"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Left sub-plot: regression line for has_engaged versus conversion_rate
    sns.regplot(data=df, x="has_engaged", y="conversion_rate", ax=ax1, seed=42)
    ax1.set_title("Engagement Rate vs Conversion Rate")
    ax1.set_xlabel("Engagement Rate (%)")
    ax1.set_ylabel("Conversion Rate (%)")
    ax1.annotate(f'Correlation: {correlation:.2f}', xy=(0.05, 0.95), xycoords='axes fraction', fontsize=12, color='red', ha='left', va='top')

    # Right sub-plot: scatter plot for has_engaged versus conversion_rate, colored
    # by campaign type
    sns.scatterplot(data=df, x="has_engaged", y="conversion_rate", hue="type", ax=ax2)
    ax2.set_title("Engagement Rate vs Conversion Rate")
    ax2.set_xlabel("Engagement Rate (%)")
    ax2.set_ylabel("Conversion Rate (%)")

    plt.tight_layout()
    plt.savefig(f"{VISUALS_PATH}/engagement_vs_conversion_rate.png", bbox_inches="tight", dpi=300)
    plt.close()

def analyze_clv_conversion(campaign_customers_df, campaigns_df):
    """
    Analyze the relationship between CLV exposure and conversion rate.
    
    Args:
        campaign_customers_df (DataFrame): Combined dataframe with campaign and customer data
        campaigns_df (DataFrame): Campaign data
    """
    campaign_cltv_exposure = campaign_customers_df.groupby("campaign_id")["customer_lifetime_value"].sum()
    df = campaigns_df.merge(campaign_cltv_exposure, on="campaign_id")
    df["conversion_rate"] = df["conversion_rate"] * 100

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="customer_lifetime_value", y="conversion_rate")
    plt.title("Conversion Rate vs CLV per campaign")
    plt.xlabel("Total Customer Lifetime Value Exposure ($)")
    plt.ylabel("Conversion Rate (%)")
    plt.savefig(f"{VISUALS_PATH}/clv_exposure_vs_conversion_rate.png", bbox_inches="tight", dpi=300)
    plt.close()

def analyze_segment_distribution(campaign_customers_df):
    """
    Analyze the distribution of customer segments across campaigns.
    
    Args:
        campaign_customers_df (DataFrame): Combined dataframe with campaign and customer data
    """
    # Group by campaign_id and Segment to get the count of each segment in each campaign
    segment_distribution = campaign_customers_df.groupby(["campaign_id", "Segment"]).size().unstack(fill_value=0)

    # Plot the distribution of segments in each campaign
    plt.figure(figsize=(20, 10))
    segment_distribution.plot(kind='bar', stacked=True, figsize=(20, 10), width=0.8)  # Adjust the width parameter

    plt.title('Distribution of Customer Segments in Each Campaign')
    plt.xlabel('Campaign ID')
    plt.ylabel('Number of Customers')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{VISUALS_PATH}/segment_distribution_by_campaign.png", bbox_inches="tight", dpi=300)
    plt.close()

def main():
    """
    Main function to execute the campaign impact analysis.
    """
    # Load all data
    (campaigns_df, customer_df, digital_usage_df, engagement_details_df, 
     loans_df, products_owned_df, transactions_df, segmentation_df) = load_data()
    
    # Create a merged dataframe for campaign customer analysis
    campaign_customers_df = engagement_details_df.merge(campaigns_df, on="campaign_id").merge(
        customer_df, on="customer_id").merge(segmentation_df, on="customer_id")
    
    # Run all analyses
    analyze_campaign_target_audience(campaign_customers_df)
    
    # Print the first few rows of the target audience and age data
    print(campaign_customers_df[["target_audience", "age"]].head(10))
    
    analyze_age_mismatch(campaign_customers_df)
    analyze_engagement_rates(engagement_details_df, campaigns_df)
    analyze_monthly_engagement(campaign_customers_df)
    analyze_engagement_conversion_correlation(engagement_details_df, campaigns_df)
    analyze_clv_conversion(campaign_customers_df, campaigns_df)
    analyze_segment_distribution(campaign_customers_df)

if __name__ == '__main__':
    main()