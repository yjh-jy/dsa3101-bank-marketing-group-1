import pandas as pd
import eda_functions as eda
from load_data import load_customer_data
from feature_engineering import (create_customer_engagement_flag,
                                 summarize_transactions,
                                 engineer_digital_usage,
                                 count_products_owned
                                 )
from business_rules import define_high_value_user, is_recently_active, is_multichannel_user
from data_quality import print_null_summary, print_shape_and_preview, check_post_merge_nulls, impute_missing_values

# Load data
engagement_details, customers, digital_usage, products_owned, transactions = load_customer_data()
target_col = "has_engaged"

# EDA plots
eda.plot_numeric_distributions(customers, prefix="customers")
eda.plot_numeric_distributions(digital_usage, prefix="customers")
eda.plot_product_ownership_barplot(products_owned, "customer_id")

# Feature Engineering
customer_engagement = create_customer_engagement_flag(engagement_details)
print_null_summary(customer_engagement, "customer_engagement")
print_shape_and_preview(customer_engagement, "customer_engagement")

transaction_summary = summarize_transactions(transactions)
test_df = customer_engagement.merge(transaction_summary, on='customer_id', how='left')
check_post_merge_nulls(test_df, ["last_transaction_date"], "Engagement + Transactions")

# Digital usage transformation
digital_usage = engineer_digital_usage(digital_usage)
print_null_summary(digital_usage, "digital_usage")
print_shape_and_preview(digital_usage, "digital_usage")

eda.check_missing_correlation(digital_usage, "days_since_mobile_use", "has_mobile_app")
eda.check_missing_correlation(digital_usage, "days_since_web_use", "has_web_account")

# Products owned
products_owned = count_products_owned(products_owned)
print_null_summary(products_owned, "products_owned")
print_shape_and_preview(products_owned, "products_owned")

# Merge all features
combined_df = (
    customers
    .merge(customer_engagement, on="customer_id", how="left")
    .merge(digital_usage, on="customer_id", how="left")
    .merge(transaction_summary, on="customer_id", how="left")
    .merge(products_owned[["customer_id", "num_products_owned"]], on="customer_id", how="left")
)

# High-value user flag
combined_df["is_high_value_user"] = define_high_value_user(combined_df)
# Active in the last 30 days flag
combined_df["is_recently_active"] = is_recently_active(combined_df, days=30)
# Customers with both mobile and web usage flag
combined_df["is_multichannel_user"] = is_multichannel_user(combined_df)

# Transaction frequency
combined_df["transaction_frequency"] = combined_df["transaction_count"] / combined_df["tenure"]
combined_df[["total_transaction_amt", "transaction_count", "transaction_frequency"]] = combined_df[[
    "total_transaction_amt", "transaction_count", "transaction_frequency"]].fillna(0)
combined_df.drop(columns=["last_transaction_date"], inplace=True)

# Final checks
print_null_summary(combined_df, "combined_df")
print_shape_and_preview(combined_df, "combined_df")

# Value counts for categorical variables
categorical_cols = eda.get_categorical_columns(combined_df)
for col in categorical_cols:
    print(f"Value counts for {col}:\n{combined_df[col].value_counts()}")

# Impute missing values
combined_df = impute_missing_values(combined_df)

# Relationship Analysis
df = combined_df.copy()
target_col = "has_engaged"

eda.get_boxplot(df, target_col)
print("T-test Results:\n", eda.get_ttest(df, target_col))
eda.get_proportion_table(df, target_col)
eda.get_barplot(df, target_col)
print("\nChi-Square Test Results:\n", eda.get_chi_square(df, target_col))



#~54% of customers have never transacted
#This may include inactive, new, or digitally engaged but not monetized customers