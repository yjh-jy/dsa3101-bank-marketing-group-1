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
df = pd.merge(segments, customers, on = 'customer_id')

categorical_columns = ['job', 'marital', 'education']
for col in categorical_columns:
    df[col] = df[col].astype('category')

nps_bins = [-float('inf'), 6, 8, 10]
nps_labels = ['detractor', 'passive', 'promoter']
df['nps_category'] = pd.cut(df['nps'], bins=nps_bins, labels=nps_labels)
df.drop(['nps'], axis=1, inplace=True)
df['log_balance'] = np.sign(df['balance']) * np.log1p(np.abs(df['balance']))
df['log_debt'] = np.log1p(df['debt'])
df['log_income'] = np.log1p(df['income'])
df['debt_to_income'] = df['log_debt'] / df['log_income']
df['balance_to_debt'] = df['log_balance'] / df['log_debt']

loans['due_date'] = pd.to_datetime(loans['due_date'])
loans['paid_off_date'] = pd.to_datetime(loans['paid_off_date'])
loans['days_past_due'] = (loans['paid_off_date'] - loans['due_date']).dt.days
loans['days_past_due'] = loans['days_past_due'].fillna(0)
loans.drop(['due_date', 'paid_off_date'], axis=1, inplace=True)

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
    elif purpose == 'other':
        return 'Miscellaneous'
    else:
        return 'Uncategorized'  
loans['loan_category'] = loans['loan_purpose'].apply(categorize_loan_purpose)

transactions['transaction_type'] = transactions['transaction_type'].astype('category')
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])
transactions['transaction_date'] = transactions['transaction_date'].dt.date
transactions['transaction_date'] = pd.to_datetime(transactions['transaction_date'])

def classify_money_flow(tx_type):
    if tx_type in ['Credit', 'Deposit']:
        return 'Money In'
    else:
        return 'Money Out'
transactions['money_flow'] = transactions['transaction_type'].apply(classify_money_flow)

digital_usage['last_mobile_use'] = pd.to_datetime(digital_usage['last_mobile_use'])
digital_usage['last_web_use'] = pd.to_datetime(digital_usage['last_web_use'])

df = df.merge(products, on = 'customer_id')
df = df.merge(loans, on = 'customer_id')
df = df.merge(transactions, on = 'customer_id')
df = df.merge(digital_usage, on = 'customer_id')

# Analyzing NPS across customer segments
nps_segment_dist = pd.crosstab(df['Segment'], df['nps_category'], normalize='index') * 100
print(nps_segment_dist)

# Analyzing financial health across customer segments
variables = ['log_balance', 'log_debt', 'log_income', 'debt_to_income', 'balance_to_debt']
correlation_matrix = df[variables].corr()
print(correlation_matrix)

## filtering data for customers with days_past_due = 0
on_time = df[df['days_past_due'] == 0]
print(on_time)

## calculating the proportion of on-time payers in each segment
on_time_counts = on_time.groupby('Segment').size()
total_counts = df.groupby('Segment').size()
on_time_proportion = (on_time_counts / total_counts) * 100
print(on_time_proportion)

## loan categorization distribution by segment
loan_cat_percent = pd.crosstab(df['Segment'], df['loan_category'], normalize='index') * 100
print(loan_cat_percent)

# Analyzing product usage across customer segments
product_columns = ['has_investment_product', 'has_credit_card', 
                   'has_personal_loan', 'has_fixed_deposit', 'has_insurance']

usage_summary = df.groupby('Segment')[product_columns].mean()
print(usage_summary)

## chi-square test for the statistical significance in difference in usage across segments
for product in product_columns:
    print(f"Chi-Square Test for {product}")
    
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
## count of transactions per segment
tx_counts = df.groupby('Segment').size().reset_index(name='tx_count')
print(tx_counts)

## transaction count per customer
customer_tx = df.groupby(['customer_id', 'Segment']).size().reset_index(name='tx_count')
print(customer_tx)

## the average transaction count per segment
avg_tx_count_by_segment = customer_tx.groupby('Segment')['tx_count'].mean().reset_index()
print(avg_tx_count_by_segment)

## cross-tabulation for the distribution of transaction types across segments
tx_type_distribution = pd.crosstab(df['Segment'], df['transaction_type'])
print(tx_type_distribution)

## the frequency of each transaction type for every customer segment, with the counts normalized row-wise
tx_type_percent = pd.crosstab(df['Segment'], df['transaction_type'], normalize='index') * 100
print(tx_type_percent)

## cross-tabulation for the distribution of money flow across segments
flow_distribution = pd.crosstab(df['Segment'], df['money_flow'])
print(flow_distribution)

flow_percent = pd.crosstab(df['Segment'], df['money_flow'], normalize='index') * 100
print(flow_percent)

## grouping the data by segment and money_flow, and summing the transaction amounts
money_summary = df.groupby(['Segment', 'money_flow'])['transaction_amt'].sum().reset_index()
print(money_summary)

## calculating the percentage of each money_flow type within each segment
money_summary['percentage'] = money_summary.groupby('Segment')['transaction_amt'].transform(lambda x: x / x.sum() * 100)

## calculating the percentage of transaction counts for money in vs. money out across segments
flow_percent.reset_index(inplace=True)
flow_percent_melted = flow_percent.melt(id_vars='Segment', var_name='money_flow', value_name='percentage')
print(flow_percent_melted)

# Analyzing digital engagement across customer segments
## grouping by segment and computing the most recent usage date
recency_metrics = df.groupby('Segment').agg({
    'last_mobile_use': 'max',
    'last_web_use': 'max'
})

## identifying inactive users (no mobile or web logins)
inactive_users = df[(df['mobile_logins_wk'] == 0) & (df['web_logins_wk'] == 0)]
inactive_by_segment = inactive_users.groupby('Segment').size()
print(inactive_by_segment)