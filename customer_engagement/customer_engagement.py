# Load packages
import pandas as pd
import eda_functions as eda

# Load datasets
engagement_df = pd.read_csv("../data/processed/engagement_details.csv")
campaign_df = pd.read_csv("../data/processed/campaigns.csv")
customer_df = pd.read_csv("../data/processed/customer.csv")
digital_usage_df = pd.read_csv("../data/processed/digital_usage.csv")
products_owned_df = pd.read_csv("../data/processed/products_owned.csv")
transactions_df = pd.read_csv("../data/processed/transactions.csv")

# Keep only relevant features
# Convert to datetime format
transactions_df['transaction_date'] = pd.to_datetime( 
    transactions_df['transaction_date'], format="%Y-%m-%d %H:%M:%S")
digital_usage_df['last_mobile_use'] = pd.to_datetime(
    digital_usage_df['last_mobile_use'], format="%Y-%m-%d")
digital_usage_df['last_web_use'] = pd.to_datetime( 
    digital_usage_df['last_web_use'], format="%Y-%m-%d")

# Get most recent transaction per customer
last_transaction_df = transactions_df.groupby('customer_id', as_index=False)['transaction_date'].max()
last_transaction_df = last_transaction_df.rename(columns={'transaction_date': 'last_transaction_date'})

# Convert date fields to days since xxx format
reference_date = pd.to_datetime('2025-01-01')
transactions_df['days_since_transaction'] = (reference_date - transactions_df['transaction_date']).dt.days
digital_usage_df['days_since_mobile_use'] = (reference_date - digital_usage_df['last_mobile_use']).dt.days
digital_usage_df['days_since_web_use'] = (reference_date - digital_usage_df['last_web_use']).dt.days

# Drop original datetime columns
transactions_df = transactions_df.drop(columns=['transaction_date'])
digital_usage_df = digital_usage_df.drop(columns=['last_mobile_use', 'last_web_use'])

engagement_df = engagement_df[[ 'customer_id', 'campaign_id', 'channel_used', 'has_engaged']]
campaign_df = campaign_df[[ 'campaign_id', 'campaign_type', 'campaign_duration', 
                            'campaign_language', 'impressions', 'clicks']]
customer_df = customer_df.drop(columns='default')

# Get percentage of null values in column last_transaction_date
test_df = engagement_df.merge(last_transaction_df, on='customer_id', how='left')
null_percentages_test= test_df.isnull().mean().round(4) * 100
null_percentages_test = null_percentages_test.sort_values(ascending=False)
print(null_percentages_test)

# Filter rows with missing values
missing_rows_df = test_df[test_df['last_transaction_date'].isnull()]

# Count occurrences of 0 and 1 for has_engaged in missing data
has_engaged_counts = missing_rows_df['has_engaged'].value_counts()
print(has_engaged_counts)

# Calculate percentages
has_engaged_percentages = has_engaged_counts / len(missing_rows_df) * 100
print(has_engaged_percentages)

# Merge files
combined_df = engagement_df.merge(campaign_df, on='campaign_id', how='left')
combined_df = combined_df.merge(customer_df, on='customer_id', how='left')
combined_df = combined_df.merge(digital_usage_df, on='customer_id', how='left')
combined_df = combined_df.merge(products_owned_df, on='customer_id', how='left')
#combined_df = combined_df.merge(last_transaction_df, on='customer_id', how='left')

# Drop ID columns
combined_df = combined_df.drop(columns=['customer_id', 'campaign_id'])

null_percentages = combined_df.isnull().mean().round(4) * 100
null_percentages = null_percentages.sort_values(ascending=False)
print(null_percentages)

# Check missing mobile logins correlation with has_mobile_app
print(eda.check_missing_correlation(combined_df, 'mobile_logins_wk', 'has_mobile_app'))

# Check missing web logins correlation with has_web_account
print(eda.check_missing_correlation(combined_df, 'web_logins_wk', 'has_web_account'))

# Check missing avg_mobile_time correlation with has_mobile_app
print(eda.check_missing_correlation(combined_df, 'avg_mobile_time', 'has_mobile_app'))

# Check missing avg_web_time correlation with has_web_account
print(eda.check_missing_correlation(combined_df, 'avg_web_time', 'has_web_account'))

# Check missing days_since_mobile_use correlation with has_mobile_app
print(eda.check_missing_correlation(combined_df, 'days_since_mobile_use', 'has_mobile_app'))

# Check missing days_since_web_use correlation with has_web_account
print(eda.check_missing_correlation(combined_df, 'days_since_web_use', 'has_web_account'))


# Drop rows where has_mobile_app or has_web_account is NaN
combined_df = combined_df.dropna(subset=['has_mobile_app', 'has_web_account'])

# Fill NaNs with 0 for digital activity columns
cols_to_fill_zero = ['mobile_logins_wk', 'web_logins_wk', 'avg_mobile_time', 'avg_web_time', 'clicks']
combined_df[cols_to_fill_zero] = combined_df[cols_to_fill_zero].fillna(0)

# Assign a large number to indicate extreme inactivity
combined_df['days_since_mobile_use'] = combined_df['days_since_mobile_use'].fillna(9999)
combined_df['days_since_web_use'] = combined_df['days_since_web_use'].fillna(9999)


# Set df and target column
df = combined_df.copy()
target_col = 'has_engaged'

# 1. Boxplots for numerical variables by engagement
eda.get_boxplot(df, target_col)

# 2. T-tests for numerical variables
ttest_results = eda.get_ttest(df, target_col)
print("T-test Results:\n", ttest_results)

# 3. Identify categorical columns (excluding the target)
cat_cols = df.select_dtypes(include='object').columns.tolist()
cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 10 and 
             df[col].dtype in ['int64', 'float64'] and col != target_col]

cat_cols = list(set(cat_cols) - {target_col})

# 4. Proportion tables & bar plots
for col in cat_cols:
    print(f"\nProportion Table for {col}:")
    print(eda.get_proportion_table(df, col, target_col))
    
    eda.get_barplot(df, col, target_col)

# 5. Chi-square test results
chi2_results = eda.get_chi_square(df, cat_cols, target_col)
print("\nChi-Square Test Results:\n", chi2_results)