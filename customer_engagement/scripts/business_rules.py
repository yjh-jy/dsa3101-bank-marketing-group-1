import pandas as pd

def define_high_value_user(df):
    """
    Flags customer as high-value user if they are above median in both logins and spend.

    Args:
        df (pd.DataFrame): Customer-level dataframe with login and spend information.

    Returns:
        pd.Series: Binary flag (1 = high-value user, 0 = not high-value).
    """
    # Compute median login frequency and transaction amount
    login_median = df["total_logins_per_week"].median()
    spend_median = df["total_transaction_amt"].median()

    # Flag users who exceed both medians
    return ((df["total_logins_per_week"] > login_median) &
            (df["total_transaction_amt"] > spend_median)).astype(int)


def is_recently_active(df, days=30, reference_date="2025-01-01"):
    """
    Flags customers as recently active if they transacted or 
    used digital services within the past `days`.

    Args:
        df (pd.DataFrame): Customer-level dataframe with usage and transaction recency.
        days (int): Recency threshold in days.
        reference_date (str): Reference date for activity.

    Returns:
        pd.Series: Binary flag (1 = recently active, 0 = not active).
    """
    # Convert reference date to datetime
    ref_date = pd.to_datetime(reference_date)

    # Check if user used mobile or web within threshold
    recent_mobile = df["days_since_mobile_use"] <= days
    recent_web = df["days_since_web_use"] <= days

    # Check if transaction frequency is non-zero
    recent_transaction = df["transaction_frequency"] > 0

    # Flag if any condition is satisfied
    return (recent_mobile | recent_web | recent_transaction).astype(int)


def is_multichannel_user(df):
    """
    Flags customers who have used both mobile and web channels.

    Args:
        df (pd.DataFrame): Customer-level dataframe with channel usage recency.

    Returns:
        pd.Series: Binary flag (1 = multichannel user, 0 = single/no channel).
    """
    # Flag users who have used both mobile and web (days_since < 999)
    return ((df["days_since_mobile_use"] < 999) & (df["days_since_web_use"] < 999)).astype(int)