# Customer-Level EDA
'''
This script analyses customer attributes in relation to engagement outcomes,
focusing on behavioural, financial, and digital activity indicators that may 
drive customer responsiveness.
'''

import utils as ut
from feature_engineering import (create_customer_engagement_flag,
                                 summarize_transactions,
                                 engineer_digital_usage,
                                 count_products_owned
                                 )
from business_rules import define_high_value_user, is_recently_active, is_multichannel_user

# Global constants
target_col = "has_engaged"

def main():
    '''
    Main function to execute customer-level exploratory data analysis (EDA).
    '''

    # Load data
    engagement_details, customers, digital_usage, products_owned, transactions = ut.load_customer_data()

    # EDA plots
    ut.plot_numeric_distributions(customers, prefix="customers")
    ut.plot_numeric_distributions(digital_usage, prefix="customers")
    ut.plot_product_ownership_barplot(products_owned, "customer_id")

    # Feature Engineering
    customer_engagement = create_customer_engagement_flag(engagement_details)
    ut.print_null_summary(customer_engagement, "customer_engagement")
    ut.print_shape_and_preview(customer_engagement, "customer_engagement")

    transaction_summary = summarize_transactions(transactions)
    test_df = customer_engagement.merge(transaction_summary, on='customer_id', how='left')
    ut.check_post_merge_nulls(test_df, ["last_transaction_date"], "Engagement + Transactions")

    # Digital usage transformation
    digital_usage = engineer_digital_usage(digital_usage)
    ut.print_null_summary(digital_usage, "digital_usage")
    ut.print_shape_and_preview(digital_usage, "digital_usage")

    # Check correlation between missing values in digital usage data
    ut.check_missing_correlation(digital_usage, "days_since_mobile_use", "has_mobile_app")
    ut.check_missing_correlation(digital_usage, "days_since_web_use", "has_web_account")

    # Products owned
    products_owned = count_products_owned(products_owned)
    ut.print_null_summary(products_owned, "products_owned")
    ut.print_shape_and_preview(products_owned, "products_owned")

    # Merge all features into a single dataframe
    combined_df = (
        customers
        .merge(customer_engagement, on="customer_id", how="left")
        .merge(digital_usage, on="customer_id", how="left")
        .merge(transaction_summary, on="customer_id", how="left")
        .merge(products_owned[["customer_id", "num_products_owned"]], on="customer_id", how="left")
    )

    # Feature engineering for additional attributes
    combined_df["is_high_value_user"] = define_high_value_user(combined_df)
    combined_df["transaction_frequency"] = combined_df["transaction_count"] / combined_df["tenure"]
    combined_df[["total_transaction_amt", "transaction_count", "transaction_frequency"]] = combined_df[[
        "total_transaction_amt", "transaction_count", "transaction_frequency"]].fillna(0) # Fill missing values with zero
    combined_df.drop(columns=["last_transaction_date"], inplace=True)
    # Flags for customer activity
    combined_df["is_recently_active"] = is_recently_active(combined_df, days=30)
    combined_df["is_multichannel_user"] = is_multichannel_user(combined_df)

    # Final dataset checks
    ut.print_null_summary(combined_df, "combined_df")
    ut.print_shape_and_preview(combined_df, "combined_df")

    # Value counts for categorical variables
    categorical_cols = ut.get_categorical_columns(combined_df)
    for col in categorical_cols:
        print(f"Value counts for {col}:\n{combined_df[col].value_counts()}")

    # Impute missing values
    combined_df = ut.impute_missing_values(combined_df)

    # Relationship Analysis (against target variable)
    df = combined_df.copy()
    ut.get_boxplot(df, target_col)
    print("T-test Results:\n", ut.get_ttest(df, target_col))
    ut.get_proportion_table(df, target_col)
    ut.get_barplot(df, target_col)
    print("\nChi-Square Test Results:\n", ut.get_chi_square(df, target_col))

    # Multivariate Exploration
    
    # Select numerical & boolean feature for analysis
    multivariate_features = [col for col in df.columns 
                             if col != target_col and 
                             df[col].dtype in ["int64", "float64", "int32", "bool"]]

    # Run multivariate exploratory analysis model
    ut.run_multivariate_exploration(df,
                                    target_col='has_engaged',
                                    feature_cols=multivariate_features
                                    )

if __name__ == "__main__":
    main()