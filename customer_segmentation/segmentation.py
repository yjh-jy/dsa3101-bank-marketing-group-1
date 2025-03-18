# Customer segmentation into 4 categories ("High-value", "At risk / inactive customers", "Occasional", "Budget-conscious")
## Importing packages
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score


## READING IN DATA
customer_df = pd.read_csv("data/processed/customer.csv")
digital_usage_df = pd.read_csv("data/processed/digital_usage.csv")
transactions_df = pd.read_csv("data/processed/transactions.csv")
loans_df = pd.read_csv("data/processed/loans.csv")
products_df = pd.read_csv("data/processed/products_owned.csv")

## ENSURE DATES ARE IN RIGHT FORMAT
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"])
loans_df["due_date"] = pd.to_datetime(loans_df["due_date"])
loans_df["paid_off_date"] = pd.to_datetime(loans_df["paid_off_date"])

## CREATING INTERACTION TERMS
### Calculate days_from_last_transaction
latest_transaction = transactions_df.groupby("customer_id")["transaction_date"].max().reset_index()
latest_transaction["days_from_last_transaction"] = (pd.to_datetime("today") - latest_transaction["transaction_date"]).dt.days
latest_transaction = latest_transaction[["customer_id", "days_from_last_transaction"]]
### Calculate avg_transaction_amt per customer
transaction_summary = transactions_df.groupby("customer_id").agg(total_transaction_amt=("transaction_amt", "sum"),num_transactions=("transaction_id", "count")).reset_index()
transaction_summary["avg_transaction_amt"] = transaction_summary["total_transaction_amt"] / transaction_summary["num_transactions"]
transaction_summary = transaction_summary[["customer_id", "avg_transaction_amt"]]

scaler = MinMaxScaler()

### Calculate digital engagement score
digital_usage_df["normalized_logins"] = scaler.fit_transform(digital_usage_df[["mobile_logins_wk", "web_logins_wk"]].sum(axis=1).values.reshape(-1, 1))
digital_usage_df["normalized_session_time"] = scaler.fit_transform(digital_usage_df[["avg_mobile_time", "avg_web_time"]].sum(axis=1).values.reshape(-1, 1))
digital_usage_df["digital_engagement_score"] = (digital_usage_df["normalized_logins"] * 0.7 +digital_usage_df["normalized_session_time"] * 0.3)
### Correct aggregation step
digital_engagement = digital_usage_df.groupby("customer_id", as_index=False)["digital_engagement_score"].mean()

### Median loan repayment time per customer
loans_df["loan_repayment_time"] = (loans_df["paid_off_date"] - loans_df["due_date"]).dt.days
loan_summary = loans_df.groupby("customer_id")["loan_repayment_time"].median().reset_index()

### Total products owned
products_df["total_products_owned"] = products_df.iloc[:, 1:].sum(axis=1)
products_summary = products_df[["customer_id", "total_products_owned"]]

## Extracting relevant columns from customer table
customer_features = ['customer_id', 'income', 'balance', 'customer_lifetime_value', 'debt', 'tenure', 'default']
customer_subset_df = customer_df[customer_features]

## MERGE DATASETS
df = customer_subset_df.merge(latest_transaction, on="customer_id", how="left")
df = df.merge(transaction_summary[["customer_id", "avg_transaction_amt"]], on="customer_id", how="left")
df = df.merge(digital_engagement[["customer_id", "digital_engagement_score"]], on="customer_id", how="left")
df = df.merge(loan_summary, on="customer_id", how="left")
df = df.merge(products_df[["customer_id", "total_products_owned"]], on="customer_id", how="left")

print(df.isnull().sum())

## HANDLING MISSING VALUES
### engagement score only has 19 missing values
df["digital_engagement_score"] = KNNImputer(n_neighbors=5).fit_transform(df[["digital_engagement_score"]])
### no transaction record (we set transactions to be 0)
df["avg_transaction_amt"].fillna(0, inplace=True)
### some did not do transactions. we set the days from last transaction to be a high but not too extreme value. We add 2 months of buffer
df["days_from_last_transaction"].fillna(df["days_from_last_transaction"].max() + 30, inplace=True)
### clients who did not loan before, we set has_loan variable to 0. for those that has loaned but hasnt repaid will have repayment time of max repayment time + buffer of a month
df["has_loan"] = df["customer_id"].isin(loans_df["customer_id"]).astype(int)
loan_repay_max = df["loan_repayment_time"].max()
df["loan_repayment_time"] = df.apply(lambda row: 0 if row["has_loan"] == 0 else (loan_repay_max + 30 if np.isnan(row["loan_repayment_time"]) else row["loan_repayment_time"]),axis=1)

print(df.isnull().sum())

## STANDARDIZING FOR K-MEANS CLUSTERING
scaler = StandardScaler()
features_to_scale = ["income", "balance", "customer_lifetime_value", "debt", "days_from_last_transaction", "avg_transaction_amt", "digital_engagement_score", "total_products_owned", "loan_repayment_time"]
df_scaled = scaler.fit_transform(df[features_to_scale])

features = df.columns

## K-MEANS CLUSTERING
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
df["Cluster"] = kmeans.fit_predict(df_scaled)

### Number of clients in each cluster
print(df["Cluster"].value_counts())

### Get information about each cluster
print(df.groupby("Cluster")[features].mean())

### Based on mean of features (1 = High value, 2 = At risk / inactive customers, 3 = "Occasional", 0 = "Budget conscious" )
segment_mapping = {
    1: "High-value",
    2: "At risk / inactive customers",
    3: "Occasional",
    0: "Budget-conscious"
}

customer_segments = df[["customer_id", "Cluster"]].copy()
customer_segments["Segment"] = customer_segments["Cluster"].map(segment_mapping)

### Drop 'Cluster' column
customer_segments.drop(columns=["Cluster"], inplace=True)

print(customer_segments.head())

## Creates csv table in under customer segmentation
customer_segments.to_csv("customer_segmentation/customer_segments.csv", index=False)
print("Saved 'customer_segments.csv' with Customer ID & segment name")
