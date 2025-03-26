# Key insights and targeted marketing approaches for each customer segment are included in the notebook

# Importing packages
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

# Reading in datasets
customers = pd.read_csv("r/../data/processed/customer.csv")
digital_usage = pd.read_csv("r/../data/processed/digital_usage.csv")
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

plt.figure(figsize=(8, 6))
ax = nps_segment_dist.plot(kind='bar', stacked=True)
plt.title('Distribution of NPS Categories Across Customer Segments')
plt.xlabel('Customer Segment')
plt.ylabel('Percentage (%)')
plt.legend(title='NPS Category', bbox_to_anchor=(1.05, 1), loc='upper left')

for p in ax.patches:
    height = p.get_height()
    width = p.get_width()
    x = p.get_x() + width / 2
    y = p.get_y() + height / 2
    ax.annotate(f'{height:.2f}%', (x, y), ha='center', va='center', color='black', fontsize=10)

plt.tight_layout()
#plt.show()

# Analyzing financial health across customer segments
## Computing the correlation matrix for the selected variables to assess relationships between them
variables = ['log_balance', 'log_debt', 'log_income', 'debt_to_income', 'balance_to_debt']
correlation_matrix = df[variables].corr()
print('\nCorrelation matrix for financial variables:')
print(correlation_matrix)

# Heatmap of correlation matrix for financial health metrics
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix for Financial Health Metrics')
#plt.show()

fig, ax = plt.subplots(1, 2, figsize=(14, 6))
# Boxplot of 'debt-to-income' ratio by customer segment
sns.boxplot(x='Segment', y='debt_to_income', data=df, ax=ax[0])
ax[0].set_title('Debt-to-Income Ratio by Customer Segment')
ax[0].set_xlabel('Customer Segment')
ax[0].set_ylabel('Debt-to-Income Ratio')
# Boxplot of 'balance-to-debt' ratio by customer segment
sns.boxplot(x='Segment', y='balance_to_debt', data=df, ax=ax[1])
ax[1].set_title('Balance-to-Debt Ratio by Customer Segment')
ax[1].set_xlabel('Customer Segment')
ax[1].set_ylabel('Balance-to-Debt Ratio')
plt.tight_layout()
#plt.show()

## Filtering data for customers with days_past_due < 0
on_time = df[df['days_past_due'] < 0]
print(on_time)

## Calculating the proportion of on-time payers in each segment
on_time_counts = on_time.groupby('Segment').size()
total_counts = df.groupby('Segment').size()
on_time_proportion = (on_time_counts / total_counts) * 100
print('\nProportion of on-time payers (%) in each segment:')
print(on_time_proportion)

# Bar plot of the proportion of customers with on-time loan payments for each segment
plt.figure(figsize=(8, 5))
ax = sns.barplot(x=on_time_proportion.index, y=on_time_proportion.values, palette='viridis')
plt.title('Proportion of On-Time Loan Payments Across Customer Segments')
plt.xlabel('Customer Segments')
plt.ylabel('Proportion of On-Time Payments (%)')
plt.ylim(0, 100)
plt.grid(axis='y')
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}%', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                color='black', fontsize=10, 
                xytext=(0, 5), textcoords='offset points')  
#plt.tight_layout()
#plt.show()

## Calculating the percentage distribution of loan categories within each segment
loan_cat_percent = pd.crosstab(df['Segment'], df['loan_category'], normalize='index') * 100
print('\nPercentage distribution of loan categories within each segment:')
print(loan_cat_percent)

# Analyzing product usage across customer segments
## Calculating the average product ownership for each segment across specified product columns
product_columns = ['has_investment_product', 'has_credit_card', 
                   'has_fixed_deposit', 'has_insurance']
usage_summary = df.groupby('Segment')[product_columns].mean()
print('\nAverage product ownership (%) for each segment:')
print(usage_summary)

# Barplot of product usage proportions by customer segment
usage_summary_reset = usage_summary.reset_index()
usage_melted = usage_summary_reset.melt(id_vars='Segment', 
                                         var_name='Product', 
                                         value_name='Proportion')
plt.figure(figsize=(12, 6))
ax = sns.barplot(data=usage_melted, x='Product', y='Proportion', hue='Segment')
plt.title('Product Usage Proportions by Customer Segment')
plt.ylabel('Proportion of Customers Owning Product')
plt.xlabel('Product')
plt.legend(title='Segment')
plt.xticks(rotation=45)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='center', 
                color='black', fontsize=10, 
                xytext=(0, 5), textcoords='offset points')  
#plt.tight_layout()
#plt.show()

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

## Calculating the distribution of money flow across segments
flow_distribution = pd.crosstab(df['Segment'], df['money_flow'])
print('\nDistribution of money flow across segments:')
print(flow_distribution)

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# Barplot of the average transaction count by customer segment
sns.barplot(data=avg_tx_count_by_segment, x='Segment', y='tx_count', palette='viridis', ax=ax[0])
ax[0].set_xlabel('Customer Segment')
ax[0].set_ylabel('Average Transaction Count')
ax[0].set_title('Average Transaction Count by Customer Segment')

for p in ax[0].patches:
    ax[0].annotate(f'{p.get_height():.2f}', 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='center', 
                   color='black', fontsize=10, 
                   xytext=(0, 5), textcoords='offset points') 

# Barplot of the average transaction value by customer segment
avg_transaction_value = df.groupby('Segment')['transaction_amt'].mean().reset_index()
bars = ax[1].bar(avg_transaction_value['Segment'], avg_transaction_value['transaction_amt'], 
                 color=['skyblue', 'lightgreen', 'lightcoral'])
ax[1].set_xlabel('Customer Segment')
ax[1].set_ylabel('Average Transaction Value')
ax[1].set_title('Average Transaction Value by Customer Segment')
for bar in bars:
    ax[1].text(bar.get_x() + bar.get_width() / 2, 
               bar.get_height(), 
               f'{bar.get_height():.2f}', 
               ha='center', 
               va='bottom', 
               fontsize=10, 
               color='black')
#plt.tight_layout()
#plt.show()

## Grouping by segment and money flow, summing the transaction amount, and calculating percentage
money_summary = df.groupby(['Segment', 'money_flow'])['transaction_amt'].sum().reset_index()
print('\nTransaction amount by segment and money flow:')
print(money_summary)

fig, ax = plt.subplots(1, 2, figsize=(18, 6))

# Barplot of transaction amount (money_summary)
sns.barplot(data=money_summary, x='Segment', y='transaction_amt', hue='money_flow', palette='viridis', ax=ax[0])

for container in ax[0].containers:
    ax[0].bar_label(container, fmt='%.2f', padding=3)

ax[0].set_xlabel('Customer Segment')
ax[0].set_ylabel('Transaction Amount')
ax[0].set_title('Transaction Amount by Money Flow Across Customer Segments')
ax[0].legend(title='Money Flow')

# Barplot of transaction count for money flow across segments
flow_distribution_reset = flow_distribution.reset_index()
flow_melted = flow_distribution_reset.melt(id_vars='Segment', var_name='money_flow', value_name='Count')
sns.barplot(data=flow_melted, x='Segment', y='Count', hue='money_flow', palette='viridis', ax=ax[1])
for container in ax[1].containers:
    ax[1].bar_label(container, padding=3)

ax[1].set_xlabel('Customer Segment')
ax[1].set_ylabel('Transaction Count')
ax[1].set_title('Transaction Count by Money Flow Across Customer Segments')
ax[1].legend(title='Money Flow')
#plt.tight_layout()
#plt.show()


## Transforming the money flow data to a long format for easier comparison across segments
flow_distribution_reset = flow_distribution.reset_index()
flow_melted = flow_distribution_reset.melt(id_vars='Segment', var_name='money_flow', value_name='Count')
print('\nMelted money flow data:')
print(flow_melted)

# Analyzing digital engagement across customer segments
fig, ax = plt.subplots(1, 2, figsize=(18, 6))
# Barplot of transaction amount (money_summary)
sns.barplot(data=money_summary, x='Segment', y='transaction_amt', hue='money_flow', palette='viridis', ax=ax[0])
for container in ax[0].containers:
    ax[0].bar_label(container, fmt='%.2f', padding=3)
ax[0].set_xlabel('Customer Segment')
ax[0].set_ylabel('Transaction Amount')
ax[0].set_title('Transaction Amount by Money Flow Across Customer Segments')
ax[0].legend(title='Money Flow')
# Barplot of transaction count for money flow across segments
flow_distribution_reset = flow_distribution.reset_index()
flow_melted = flow_distribution_reset.melt(id_vars='Segment', var_name='money_flow', value_name='Count')
sns.barplot(data=flow_melted, x='Segment', y='Count', hue='money_flow', palette='viridis', ax=ax[1])
for container in ax[1].containers:
    ax[1].bar_label(container, padding=3)
ax[1].set_xlabel('Customer Segment')
ax[1].set_ylabel('Transaction Count')
ax[1].set_title('Transaction Count by Money Flow Across Customer Segments')
ax[1].legend(title='Money Flow')
#plt.tight_layout()
#plt.show()

## Grouping by segment and computing the most recent usage date for mobile and web
recency_metrics = df.groupby('Segment').agg({
    'last_mobile_use': 'max',
    'last_web_use': 'max'
})
print('\nMost recent mobile and web usage dates by segment:')
print(recency_metrics)

# Boxplot of mobile and web engagement ratio across customer segments
sns.boxplot(x='Segment', y='mobile_web_ratio', data=df)
plt.title('Mobile vs Web Engagement Ratio Across Segments')
#plt.show()

## Identifying inactive users (those with no mobile or web logins)
inactive_users = df[(df['mobile_logins_wk'] == 0) & (df['web_logins_wk'] == 0)]
inactive_by_segment = inactive_users.groupby('Segment').size()
print('\nNumber of inactive users in each segment:')
print(inactive_by_segment)