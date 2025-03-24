# Load packages
import pandas as pd
import eda_functions as eda

# Load datasets
engagement_details = pd.read_csv("../data/processed/engagement_details.csv")
customers = pd.read_csv("../data/processed/customer.csv")
digital_usage = pd.read_csv("../data/processed/digital_usage.csv")
products_owned = pd.read_csv("../data/processed/products_owned.csv")
transactions = pd.read_csv("../data/processed/transactions.csv")

# Plot numeric distributions for customer demographics
eda.plot_numeric_distributions(customers, prefix="customers")

# Plot numeric distributions for digital usage
eda.plot_numeric_distributions(digital_usage, prefix="customers")

# Product ownership (bar plot per product)
eda.plot_product_ownership_barplot(products_owned, "customer_id")

# Create customer-level has_engaged flag (1 if engaged in any campaign)
customer_engagement = (
    engagement_details
    .groupby("customer_id")["has_engaged"]
    .max()
    .reset_index()
)

# Check for nulls in 'has_engaged' as well as customer_engagement dataframe details
null_count = customer_engagement["has_engaged"].isnull().sum()
print(f"Number of nulls in 'has_engaged': {null_count}")
print(f"\nShape of customer_engagement: {customer_engagement.shape}")
print(f"\nFirst few rows of customer_engagement:\n{customer_engagement.head()}")

# Aggregate transactions 
transaction_summary = (
    transactions
    .groupby("customer_id")
    .agg(
        total_transaction_amt=("transaction_amt", "sum"),
        transaction_count=("transaction_id", "count"),
        last_transaction_date=("transaction_date", "max")
    )
    .reset_index()
)
# Get percentage of null values in column last_transaction_date
test_df = customer_engagement.merge(transaction_summary, on='customer_id', how='left')
null_percentages_test= test_df.isnull().mean().round(4) * 100
null_percentages_test = null_percentages_test.sort_values(ascending=False)
print(f"Percentage of nulls in transaction columns after merge:\n{null_percentages_test}")
#~54% of customers have never transacted
#This may include inactive, new, or digitally engaged but not monetized customers

# Feature engineering on digital usage

# Convert to datetime format
digital_usage['last_mobile_use'] = pd.to_datetime( digital_usage['last_mobile_use'], format="%Y-%m-%d")
digital_usage['last_web_use'] = pd.to_datetime( digital_usage['last_web_use'], format="%Y-%m-%d")
# Convert date fields to days since xxx format
reference_date = pd.to_datetime('2025-01-01')
# Create new features
digital_usage['days_since_mobile_use'] = (reference_date - digital_usage['last_mobile_use']).dt.days
digital_usage['days_since_web_use'] = (reference_date - digital_usage['last_web_use']).dt.days
digital_usage["total_logins_per_week"] = digital_usage[["mobile_logins_wk", "web_logins_wk"]].sum(axis=1)
digital_usage["avg_total_time_per_session"] = digital_usage[["avg_mobile_time", "avg_web_time"]].sum(axis=1)

# Drop original columns
digital_usage = digital_usage.drop(columns=["last_mobile_use", "last_web_use",
                                            "mobile_logins_wk", "web_logins_wk",
                                            "avg_mobile_time", "avg_web_time"])
print(f"Null counts per column: \n {digital_usage.isnull().sum()}")
print(f"\nShape of digital_usage: {digital_usage.shape}")
print(f"\nFirst few rows of digital_usage:\n{digital_usage.head()}")

# Check missing days_since_mobile_use correlation with has_mobile_app
check = eda.check_missing_correlation(digital_usage, "days_since_mobile_use", "has_mobile_app")

# Check missing days_since_web_use correlation with has_web_account
check = eda.check_missing_correlation(digital_usage, "days_since_web_use", "has_web_account")

# Results interpretation: The customers who are missing days_since_mobile_use or days_since_web_use are those who never had access to the respective platforms
# Fill the missing values by assigning a large number to indicate extreme inactivity
digital_usage["days_since_mobile_use"] = digital_usage["days_since_mobile_use"].fillna(999)
digital_usage["days_since_web_use"] = digital_usage["days_since_web_use"].fillna(999)

# Feature engineering on products owned
products_owned["num_products_owned"] = products_owned.drop(columns="customer_id").sum(axis=1)

# Check for nulls in 'num_products_owned' as well as details of products_owned dataframe
null_count = products_owned["num_products_owned"].isnull().sum()
print(f"Number of nulls in 'num_products_owned': {null_count}")
print(f"\nShape of products_owned: {products_owned.shape}")
print(f"\nFirst few rows of products_owned:\n{products_owned.head()}")

# Merge all features into combined_df
combined_df = (
    customers
    .merge(customer_engagement, on="customer_id", how="left")
    .merge(digital_usage, on="customer_id", how="left")
    .merge(transaction_summary, on="customer_id", how="left")
    .merge(products_owned[["customer_id", "num_products_owned"]], on="customer_id", how="left")
)

# Create high-value user flag based on median thresholds
login_median = combined_df["total_logins_per_week"].median()
spend_median = combined_df["total_transaction_amt"].median()
combined_df["is_high_value_user"] = (
    (combined_df["total_logins_per_week"] > login_median) &
    (combined_df["total_transaction_amt"] > spend_median)
).astype(int)

# Feature: transaction frequency
combined_df["transaction_frequency"] = combined_df["transaction_count"] / combined_df["tenure"]
combined_df[["total_transaction_amt", "transaction_count", "transaction_frequency"]] = combined_df[[
    "total_transaction_amt", "transaction_count", "transaction_frequency"]].fillna(0)

combined_df = combined_df.drop(columns=["last_transaction_date"])

# Check nulls
null_counts = combined_df.isnull().sum()
null_percentages = (combined_df.isnull().mean() * 100).round(2)
null_summary = pd.DataFrame({
    "Null Count": null_counts,
    "Null %": null_percentages}).sort_values("Null %", ascending=False)
print("Null summary:\n", null_summary)
print(f"\nFirst few rows:\n {combined_df.head()}")
print("\nShape of combined_df:", combined_df.shape)
# Drop rows with null values in any column in combined_df
before = combined_df.shape[0]
combined_df = combined_df.dropna()
after = combined_df.shape[0]
print(f"Dropped {before - after} rows with nulls. Remaining rows: {after}")

# Relationship analysis with target variable `has_engaged`

# Set df and target column
df = combined_df.copy()
target_col = 'has_engaged'

# 1. Boxplots for numerical variables by engagement
eda.get_boxplot(df, target_col)

# 2. T-tests for numerical variables
ttest_results = eda.get_ttest(df, target_col)
print("T-test Results:\n", ttest_results)

# 3. Proportion tables & bar plots for categorical columns against `has_engaged`
tables = eda.get_proportion_table(df, target_col)
barplots = eda.get_barplot(df, target_col)

# 4. Chi-square test results
chi2_results = eda.get_chi_square(df, target_col)
print("\nChi-Square Test Results:\n", chi2_results)