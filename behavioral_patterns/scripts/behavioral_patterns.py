# Importing packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import scipy.stats as stats

# Reading in datasets
customers = pd.read_csv("r/../data/processed/customer.csv")
digital_usage = pd.read_csv("r/../data/processed/digital_usage.csv")
engagement = pd.read_csv("r/../data/processed/engagement_details.csv")
loans = pd.read_csv("r/../data/processed/loans.csv")
products = pd.read_csv("r/../data/processed/products_owned.csv") 
transactions = pd.read_csv("r/../data/processed/transactions.csv")
segments = pd.read_csv("r/../customer_segmentation/customer_segments.csv")

# Data preparation
## Merging segments and customers datasets
df = pd.merge(segments, customers, on = 'customer_id')

## Converting 'job', 'marital', and 'education' columns to category data type
categorical_columns = ['job', 'marital', 'education']
for col in categorical_columns:
    df[col] = df[col].astype('category')

## Creating 'nps_category' column that segments responses into promoters, passives, and detractors
nps_bins = [-float('inf'), 6, 8, 10]
nps_labels = ['detractor', 'passive', 'promoter']
df['nps_category'] = pd.cut(df['nps'], bins=nps_bins, labels=nps_labels)

## Dropping the original 'nps' column
df.drop(['nps'], axis=1, inplace=True)

## Applying log transformation to 'balance', 'debt', and 'income' to scale and stabilize the values
df['log_balance'] = np.sign(df['balance']) * np.log1p(np.abs(df['balance']))
df['log_debt'] = np.log1p(df['debt'])
df['log_income'] = np.log1p(df['income'])

## Creating 'debt-to-income' ratio and 'balance-to-debt' ratio columns
df['debt_to_income'] = df['log_debt'] / df['log_income']
df['balance_to_debt'] = df['log_balance'] / df['log_debt']

## Converting 'due_date' and 'paid_off_date' columns to datetime format
loans['due_date'] = pd.to_datetime(loans['due_date'])
loans['paid_off_date'] = pd.to_datetime(loans['paid_off_date'])

## Creating 'days_past_due' column
loans['days_past_due'] = (loans['paid_off_date'] - loans['due_date']).dt.days
loans['days_past_due'] = loans['days_past_due'].fillna(0)

## Dropping the original 'due_date' and 'paid_off_date' columns
loans.drop(['due_date', 'paid_off_date'], axis=1, inplace=True)

## Categorize loan purposes into broader categories and creating 'loan_category' column
def categorize_loan_purpose(purpose):
    if purpose == 'debt_consolidation':
        return 'Debt Management'
    elif purpose == 'credit_card':
        return 'Credit Product'
    elif purpose in ['housing-related', 'major_purchase', 'car']:
        return 'Asset Acquisition'
    elif purpose in ['small_business', 'educational']:
        return 'Business & Education'
    elif purpose in ['wedding', 'vacation', 'medical']:
        return 'Lifestyle & Personal'
    else:
        return 'Miscellaneous'  
loans['loan_category'] = loans['loan_purpose'].apply(categorize_loan_purpose)

## Converting 'transaction_type' column to category data type
transactions['transaction_type'] = transactions['transaction_type'].astype('category')

## Extracting year-month-day from 'transaction_date' and converting to datetime format
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
transactions['transaction_date'] = transactions['transaction_date'].dt.date
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

## Categorizing transactions as 'Money In' or 'Money Out', and creating 'money_flow' column
def classify_money_flow(tx_type):
    if tx_type in ['Credit', 'Deposit']:
        return 'Money In'
    else:
        return 'Money Out'
transactions['money_flow'] = transactions['transaction_type'].apply(classify_money_flow)

## Converting 'last_mobile_use' and 'last_web_use' columns to category data type
digital_usage['last_mobile_use'] = pd.to_datetime(digital_usage['last_mobile_use'])
digital_usage['last_web_use'] = pd.to_datetime(digital_usage['last_web_use'])

## Creating 'mobile_web_ratio' column
digital_usage['mobile_web_ratio'] = digital_usage['mobile_logins_wk'] / (digital_usage['web_logins_wk'])

## Merging products, loans, transactions, and digital_usage datasets with df
df = df.merge(products, on = 'customer_id')
df = df.merge(loans, on = 'customer_id')
df = df.merge(transactions, on = 'customer_id')
df = df.merge(digital_usage, on = 'customer_id')

# Analyzing NPS across customer segments
## Calculating the percentage distribution NPS categories within each segment
nps_segment_dist = pd.crosstab(df['Segment'], df['nps_category'], normalize='index') * 100
print('Percentage distribution of NPS categories within each segment:')
print(nps_segment_dist)

# Analyzing financial health across customer segments
## Computing the correlation matrix for the selected variables to assess relationships between them
variables = ['log_balance', 'log_debt', 'log_income', 'debt_to_income', 'balance_to_debt']
correlation_matrix = df[variables].corr()
print('\nCorrelation matrix for financial variables:')
print(correlation_matrix)

## Filtering data for customers with days_past_due = 0
on_time = df[df['days_past_due'] == 0]
print(on_time)

## Calculating the proportion of on-time payers in each segment
on_time_counts = on_time.groupby('Segment').size()
total_counts = df.groupby('Segment').size()
on_time_proportion = (on_time_counts / total_counts) * 100
print('\nProportion of on-time payers (%) in each segment:')
print(on_time_proportion)

## Calculating the percentage distribution of loan categories within each segment
loan_cat_percent = pd.crosstab(df['Segment'], df['loan_category'], normalize='index') * 100
print('\nPercentage distribution of loan categories within each segment:')
print(loan_cat_percent)

# Analyzing product usage across customer segments
## Calculating the average product ownership for each segment across specified product columns
product_columns = ['has_investment_product', 'has_credit_card', 
                   'has_personal_loan', 'has_fixed_deposit', 'has_insurance']
usage_summary = df.groupby('Segment')[product_columns].mean()
print('\nAverage product ownership (%) for each segment:')
print(usage_summary)

## Performing Chi-square test for statistical significance in product usage differences across segments
for product in product_columns:
    print(f"\nChi-Square Test for {product}:")
    
    ct = pd.crosstab(df['Segment'], df[product])
    print("Contingency Table:")
    print(ct)
    
    chi2, p, dof, expected = stats.chi2_contingency(ct)

    print(f"Chi-square Statistic: {chi2:.4f}")
    print(f"Degrees of Freedom: {dof}")
    print(f"p-value: {p:.4f}")
    print("Expected Frequencies:")
    print(expected)
    
    if p < 0.05:
        print("=> The difference in usage across segments is statistically significant.")
    else:
        print("=> The difference in usage across segments is not statistically significant.")

# Analyzing transaction history across customer segments
## Calculating the count of transactions for each segment
tx_counts = df.groupby('Segment').size().reset_index(name='tx_count')
print('\nTransaction count for each segment:')
print(tx_counts)

## Calculating the count of transactions for each customer in each segment
customer_tx = df.groupby(['customer_id', 'Segment']).size().reset_index(name='tx_count')
print('\nTransaction count for each customer in each segment:')
print(customer_tx)

## Calculating the average transaction count per segment
avg_tx_count_by_segment = customer_tx.groupby('Segment')['tx_count'].mean().reset_index()
print('\nAverage transaction count per segment:')
print(avg_tx_count_by_segment)

## Calculating the distribution of transaction types across segments
tx_type_distribution = pd.crosstab(df['Segment'], df['transaction_type'])
print('\nDistribution of transaction types across segments:')
print(tx_type_distribution)

## Calculating the percentage of each transaction type within each segment
tx_type_percent = pd.crosstab(df['Segment'], df['transaction_type'], normalize='index') * 100
print('\nPercentage of each transaction type within each segment:')
print(tx_type_percent)

## Calculating the distribution of money flow across segments
flow_distribution = pd.crosstab(df['Segment'], df['money_flow'])
print('\nDistribution of money flow across segments:')
print(flow_distribution)

## Calculating the percentage of money flow within each segment
flow_percent = pd.crosstab(df['Segment'], df['money_flow'], normalize='index') * 100
print('\nPercentage of money flow within each segment:')
print(flow_percent)

## Grouping by segment and money flow, summing the transaction amount, and calculating percentage
money_summary = df.groupby(['Segment', 'money_flow'])['transaction_amt'].sum().reset_index()
money_summary['percentage'] = money_summary.groupby('Segment')['transaction_amt'].transform(lambda x: x / x.sum() * 100)
print('\nTransaction amounts and their respective percentages by segment and money flow:')
print(money_summary)

## Transforming the money flow percentage data to a long format for easier comparison across segments
flow_percent.reset_index(inplace=True)
flow_percent_melted = flow_percent.melt(id_vars='Segment', var_name='money_flow', value_name='percentage')
print('\nMelted money flow percentage data:')
print(flow_percent_melted)

# Analyzing digital engagement across customer segments
## Grouping by segment and computing the most recent usage date for mobile and web
recency_metrics = df.groupby('Segment').agg({
    'last_mobile_use': 'max',
    'last_web_use': 'max'
})
print('\nMost recent mobile and web usage dates by segment:')
print(recency_metrics)

## Identifying inactive users (those with no mobile or web logins)
inactive_users = df[(df['mobile_logins_wk'] == 0) & (df['web_logins_wk'] == 0)]
inactive_by_segment = inactive_users.groupby('Segment').size()
print('\nNumber of inactive users in each segment:')
print(inactive_by_segment)