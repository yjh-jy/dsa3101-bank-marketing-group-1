import pandas as pd

def define_high_value_user(df):
    """
    Flags customer as high-value user if they are above median in both logins and spend.
    """
    login_median = df["total_logins_per_week"].median()
    spend_median = df["total_transaction_amt"].median()
    return ((df["total_logins_per_week"] > login_median) &
            (df["total_transaction_amt"] > spend_median)).astype(int)

def is_recently_active(df, days=30, reference_date="2025-01-01"):
    """
    Flags customers as recently active if they transacted or used digital services within the past `days`.
    """
    ref_date = pd.to_datetime(reference_date)
    recent_mobile = df["days_since_mobile_use"] <= days
    recent_web = df["days_since_web_use"] <= days
    recent_transaction = df["transaction_frequency"] > 0

    return (recent_mobile | recent_web | recent_transaction).astype(int)

def is_multichannel_user(df):
    """
    Flags customers who have used both mobile and web channels.
    """
    return ((df["days_since_mobile_use"] < 999) & (df["days_since_web_use"] < 999)).astype(int)
