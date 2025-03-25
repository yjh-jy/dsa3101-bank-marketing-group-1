def define_high_value_user(df):
    """
    Business Rule:
    High-value user = above median in both logins and spend.
    """
    login_median = df["total_logins_per_week"].median()
    spend_median = df["total_transaction_amt"].median()
    return ((df["total_logins_per_week"] > login_median) &
            (df["total_transaction_amt"] > spend_median)).astype(int)
