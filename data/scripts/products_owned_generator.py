import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.special import expit  
import matplotlib.pyplot as plt
import seaborn as sns


np.random.seed(42)

# Load Pre-Processed CSVs
loans_df = pd.read_csv("../processed/loans.csv", delimiter=",")
customers_df = pd.read_csv("../processed/customer.csv", delimiter=",")
transactions_df = pd.read_csv("../processed/transactions.csv", delimiter=",")

# Feature Engineering (DTI, Avg Transaction Amount, and Transaction Frequency)
# Compute Debt-to-Income Ratio (DTI)
customers_df['dti'] = customers_df['debt'] / customers_df['income']

# Compute Transaction Frequency per Customer
transaction_frequency = transactions_df.groupby('customer_id')['transaction_id'].count().reset_index()
transaction_frequency.rename(columns={'transaction_id': 'transaction_frequency'}, inplace=True)

# Merge engineered features into Customers table
customers_df = customers_df.merge(transaction_frequency, on='customer_id', how='left')

# Fill missing values (for customers with no transactions)
customers_df['transaction_frequency'] = customers_df['transaction_frequency'].fillna(0)

customers_df


# Generate Product Ownership based on Conditional Probabilities
df = pd.DataFrame({"customer_id": customers_df['customer_id']})

def scale_to_0_1(prob):
    return (prob - prob.min()) / (prob.max() - prob.min())

# Investment Product: High income, high balance, low DTI OR high CLV
investment_prob = (
    expit(customers_df['income'] / (customers_df['income'].median() *1.5)) * 0.3 +  
    (customers_df['balance'] / (customers_df['balance'].median() *1.5)) * 0.3 +  
    norm.cdf(customers_df['age'], 40, 15) * 0.4 +
    (1 - customers_df['dti']) * 0.7 +  
    (customers_df['customer_lifetime_value'] / customers_df['customer_lifetime_value'].median()) * 0.5  
)
df['has_investment_product'] = np.random.binomial(1, scale_to_0_1(investment_prob))


# Credit Card: Age, marital status, employment status
credit_card_prob = (
    norm.cdf(customers_df['age'], 35, 10) * 0.6 +  # Age distribution, assuming the average age for credit card owners is 30
    (customers_df['marital'] != 'Single') * 0.4 +  # Customers who are not single are more likely to have a credit card
    ((customers_df['job'] != 'Unemployed') & (customers_df['job'] != 'Student')) * 0.5  # Customers who are not unemployed or students
)
df['has_credit_card'] = np.random.binomial(1, scale_to_0_1(credit_card_prob))
# Ensure that if loan_purpose is 'credit card', has_credit_card is forced to 1
df.loc[loans_df['loan_purpose'] == 'credit_card', 'has_credit_card'] = 1

# Personal Loan
# Identify customers with UNPAID personal loans
personal_purposes = ["debt_consolidation", "major_purchase", "credit_card", "educational", "vacation", "wedding", "medical"]
unpaid_personal_loans = loans_df[
    loans_df['loan_purpose'].isin(personal_purposes) & loans_df['paid_off_date'].isnull()
]
df['has_personal_loan'] = df['customer_id'].isin(unpaid_personal_loans['customer_id']).astype(int)


# Fixed Deposit: High balance, long tenure, older age, and low dti
fixed_deposit_prob = (
    (customers_df['balance'] / customers_df['balance'].median()) * 0.2 +
    (customers_df['tenure'] / 240) * 0.5 +
    (customers_df['age'] / 70) * 0.3+
    (1 - customers_df['dti']) * 0.7
)
df['has_fixed_deposit'] = np.random.binomial(1, scale_to_0_1(fixed_deposit_prob))

# Insurance: Age, dependents, or moderate income
insurance_prob = (
    norm.cdf(customers_df['age'], 50, 15) * 0.3 +  
    norm.cdf(customers_df['income'], 12000, 6000) * 0.3 +  
    (customers_df['dependents'] / 3) * 0.7  
)
df['has_insurance'] = np.random.binomial(1, scale_to_0_1(insurance_prob))

# Print New Ownership Rates
print("Product Ownership Rates After Adjustments:\n", df.mean())

df


# export to data folder
df.to_csv("../processed/products_owned.csv", index=False)



# Count the number of customers who own each product
ownership_counts = df.drop(columns=['customer_id']).sum()

plt.figure(figsize=(8, 5))
sns.barplot(x=ownership_counts.index, hue=ownership_counts.index, y=ownership_counts.values, palette='viridis')
plt.title('Product Ownership Distribution')
plt.xticks(rotation=45)
plt.show()

