import pandas as pd

def create_customer_engagement_flag(df):
    """
    Returns a dataframe with the max engagement status per customer.
    Assumes 'has_engaged' is binary (0 or 1).

    Args:
        df (pd.DataFrame): Raw engagement_details dataframe.

    Returns:
        pd.DataFrame: Dataframe with one row per customer_id and has_engaged flag.
    """
    # Group by customer_id and get maximum engagement status (1 if engaged at least once)
    return df.groupby("customer_id")["has_engaged"].max().reset_index()


def summarize_transactions(df):
    """
    Aggregates transaction data per customer:
    - Total transaction amount
    - Number of transactions
    - Date of last transaction

    Args:
        df (pd.DataFrame): Transaction dataframe.

    Returns:
        pd.DataFrame: Aggregated transaction dataframe by customer_id.
    """
    # Group by customer_id and aggregate transaction metrics
    return df.groupby("customer_id").agg(
        total_transaction_amt=("transaction_amt", "sum"),
        transaction_count=("transaction_id", "count"),
        last_transaction_date=("transaction_date", "max")
    ).reset_index()


def engineer_digital_usage(df, reference_date="2025-01-01"):
    """
    Engineers digital usage features:
    - Days since last mobile/web use
    - Total logins per week
    - Average session time
    Drops raw login/time columns and fills missing usage values with 999.

    Args:
        df (pd.DataFrame): Digital usage dataframe.
        reference_date (str): Date used to compute recency.

    Returns:
        pd.DataFrame: Digital usage dataframe with engineered features.
    """
    # Convert date columns to datetime
    ref = pd.to_datetime(reference_date)
    df["last_mobile_use"] = pd.to_datetime(df["last_mobile_use"], format="%Y-%m-%d")
    df["last_web_use"] = pd.to_datetime(df["last_web_use"], format="%Y-%m-%d")

    # Calculate days since last mobile and web usage
    df["days_since_mobile_use"] = (ref - df["last_mobile_use"]).dt.days
    df["days_since_web_use"] = (ref - df["last_web_use"]).dt.days

    # Calculate total logins per week and average session time
    df["total_logins_per_week"] = df[["mobile_logins_wk", "web_logins_wk"]].sum(axis=1)
    df["avg_total_time_per_session"] = df[["avg_mobile_time", "avg_web_time"]].sum(axis=1)

    # Drop raw login and time columns
    df = df.drop(columns=["last_mobile_use", "last_web_use", "mobile_logins_wk", "web_logins_wk",
                          "avg_mobile_time", "avg_web_time"])

    # Fill missing recency values with 999
    df["days_since_mobile_use"] = df["days_since_mobile_use"].fillna(999)
    df["days_since_web_use"] = df["days_since_web_use"].fillna(999)

    return df


def count_products_owned(df):
    """
    Adds a `num_products_owned` column by summing binary product ownership flags across columns,
    excluding 'customer_id'.

    Args:
        df (pd.DataFrame): Product ownership dataframe.

    Returns:
        pd.DataFrame: Dataframe with additional num_products_owned column.
    """
    # Sum binary product ownership columns
    df["num_products_owned"] = df.drop(columns="customer_id").sum(axis=1)
    return df


def prepare_campaign_features(merged_df):
    """
    Aggregates campaign-level features by campaign ID and channel.
    Adds metrics like engagement rate, CTR, impressions/clicks per day.
    Maps months to quarters and drops duration column if present.

    Args:
        merged_df (pd.DataFrame): Merged engagement_details + campaigns dataframe.

    Returns:
        pd.DataFrame: Aggregated campaign-level dataframe with engineered features.
    """
    # Map month to quarter
    month_to_quarter = {
        "January": "Q1", "February": "Q1", "March": "Q1",
        "April": "Q2", "May": "Q2", "June": "Q2",
        "July": "Q3", "August": "Q3", "September": "Q3",
        "October": "Q4", "November": "Q4", "December": "Q4"
    }
    merged_df["quarter"] = merged_df["month"].map(month_to_quarter)

    # Fill missing clicks with 0
    merged_df["clicks"] = merged_df["clicks"].fillna(0)

    # Drop duration column if exists
    merged_df = merged_df.drop(columns="duration", errors="ignore")

    # Aggregate campaign metrics by campaign_id and channel_used
    grouped = merged_df.groupby(["campaign_id", "channel_used"]).agg(
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

    # Compute engagement rate and CTR
    grouped["engagement_rate"] = grouped["num_engaged"] / grouped["num_targeted"]
    grouped["click_through_rate"] = grouped["clicks"] / grouped["impressions"]

    # Compute daily metrics
    grouped["impressions_per_day"] = grouped["impressions"] / grouped["campaign_duration"]
    grouped["targets_per_day"] = grouped["num_targeted"] / grouped["campaign_duration"]
    grouped["clicks_per_day"] = grouped["clicks"] / grouped["campaign_duration"]

    # Drop columns no longer needed
    grouped = grouped.drop(columns=["campaign_id", "num_engaged", "num_targeted"])

    return grouped