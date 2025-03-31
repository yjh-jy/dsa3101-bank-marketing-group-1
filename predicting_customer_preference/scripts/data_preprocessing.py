import pandas as pd
import numpy as np

def preprocess_data(customer_df, loans_df, customer_segments_df, products_df):
    """
    Preprocess and merge customer, loan, segmentation, and product data.

    This function cleans the input DataFrames by converting loan date columns 
    to datetime, creating an indicator for active loans, selecting relevant features, 
    and merging them into a single DataFrame.

    Args:
        customer_df (pd.DataFrame): DataFrame containing customer data.
        loans_df (pd.DataFrame): DataFrame containing loan activity data.
        customer_segments_df (pd.DataFrame): DataFrame containing customer segmentation data.
        products_df (pd.DataFrame): DataFrame containing product ownership data.

    Returns:
        pd.DataFrame: A merged DataFrame with the selected and processed data.
    """
    # Convert loan date columns to datetime format
    loans_df["due_date"] = pd.to_datetime(loans_df["due_date"])
    loans_df["paid_off_date"] = pd.to_datetime(loans_df["paid_off_date"])

    # Create an indicator for active loans (True if paid_off_date is missing)
    loans_df['has_active_loan'] = loans_df['paid_off_date'].isnull()
    loans_agg = loans_df.groupby('customer_id')['has_active_loan'].max().reset_index()


    # Select relevant features from the customer DataFrame.
    customer_df = customer_df[['customer_id', 'age', 'job', 'marital', 'education', 'default', 
                               'balance', 'debt', 'income', 'dependents']]
    loans_agg = loans_agg[['customer_id', 'has_active_loan']]

    # Merge datasets on 'customer_id'
    df = pd.merge(customer_df, loans_agg, on="customer_id", how="left")
    df = pd.merge(df, customer_segments_df, on="customer_id", how="left")
    df = pd.merge(df, products_df, on="customer_id", how="left")

    # Fill missing active loan values with 0 and convert the indicator to integer type
    df['has_active_loan'] = df['has_active_loan'].fillna(0).astype(int)
    
    return df


def cap_outliers(df, col_name):
    """
    Cap the extreme values in a specified column at the 1st and 99th percentiles.

    Args:
        df (pd.DataFrame): DataFrame containing the column.
        col_name (str): Column name for which to cap extreme values.
    """
    lower_percentile = df[col_name].quantile(0.01)
    upper_percentile = df[col_name].quantile(0.99)
    df[col_name] = df[col_name].clip(lower=lower_percentile, upper=upper_percentile)


def log_transform(df, col_name):
    """
    Apply a log transformation to a specified column.

    Args:
        df (pd.DataFrame): DataFrame containing the column.
        col_name (str): Column name to transform.
    """
    df[col_name] = np.log1p(df[col_name])

