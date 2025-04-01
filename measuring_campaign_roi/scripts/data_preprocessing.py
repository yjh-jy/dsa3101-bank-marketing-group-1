import numpy as np
import pandas as pd

def preprocess_data(customer_df, campaigns_df, engagement_details_df):
    '''
    Merge and preprocess data to generate final campaign-level dataset.

    Parameters:
    - customer_df (DataFrame): Data about customers, includes CLV.
    - campaigns_df (DataFrame): Campaign metadata.
    - engagement_details_df (DataFrame): Engagement logs tied to campaign and customer.

    Returns:
    - df (DataFrame): Cleaned and feature-engineered dataset ready for modeling.
    '''
    
    # Merge engagement details with customer CLV
    engagement_with_clv = engagement_details_df.merge(
        customer_df[['customer_id', 'customer_lifetime_value']],
        on='customer_id', how='left'
    )

    # Compute average CLV per campaign
    avg_clv = engagement_with_clv.groupby('campaign_id', as_index=False)['customer_lifetime_value'].mean()
    avg_clv.rename(columns={'customer_lifetime_value': 'avg_clv'}, inplace=True)

    # Merge campaign data with CLV values
    merged_df = campaigns_df.merge(avg_clv, on='campaign_id', how='left')

    # Select and arrange relevant columns
    df = merged_df[[
        'campaign_id', 'campaign_type', 'target_audience', 'campaign_duration',
        'campaign_language', 'conversion_rate', 'acquisition_cost', 'avg_clv', 'roi'
    ]].copy()

    # Apply log transform to acquisition_cost for normalization
    df['log_acquisition_cost'] = np.log(df['acquisition_cost'])

    # Set target_audience as ordered categorical (optional for visual/ML purposes)
    df['target_audience'] = pd.Categorical(df['target_audience'], ordered=True)

    return df