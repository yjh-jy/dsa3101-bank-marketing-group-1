# Customer segmentation into 4 categories ("High-value", "At risk / inactive customers", "Occasional", "Budget-conscious")
## Importing packages
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns


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


### Calculate digital engagement score
scaler = MinMaxScaler() 
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
df_scaled = pd.DataFrame(df_scaled, columns=features_to_scale)


## K-MEANS CLUSTERING
optimal_k = 4
df_scaled["Cluster"] = KMeans(n_clusters= optimal_k, random_state=42).fit_predict(df_scaled)
df["Cluster"] = df_scaled["Cluster"]

### Number of clients in each cluster
print(df["Cluster"].value_counts())

### Get information about each cluster
cluster_means = df_scaled.groupby("Cluster")[features_to_scale].mean()
print(cluster_means)


# Step 1: Compute Weighted Scores
cluster_means["score"] = (
    cluster_means["income"] * 0.4 + 
    cluster_means["balance"] * 0.2 + 
    cluster_means["digital_engagement_score"] * 0.2 + 
    cluster_means["avg_transaction_amt"] * 0.1 + 
    cluster_means["total_products_owned"] * 0.1
)

# Step 2: Rank Clusters Based on Score (Descending)
sorted_clusters = cluster_means["score"].sort_values(ascending=False).index.tolist()

# Step 3: Assign Segments Based on Rank
dynamic_segment_mapping = {
    sorted_clusters[0]: "High-value",
    sorted_clusters[1]: "Occasional",
    sorted_clusters[2]: "Budget-conscious",
    sorted_clusters[3]: "At risk / inactive customers"
}

# Print cluster rankings before applying
print("\nCluster Ranking by Score (Best to Worst):")
for i, cluster in enumerate(sorted_clusters):
    print(f"Rank {i+1}: Cluster {cluster} → {dynamic_segment_mapping[cluster]}")

# Step 4: Apply Mapping to DataFrame
df["Segment"] = df["Cluster"].map(dynamic_segment_mapping)
print(df["Segment"].value_counts())

df_final = df[["customer_id", "Segment"]]

print(df_final.head())

segment_means = df.groupby("Segment")[features_to_scale].mean()

# Display the results
print("Mean of original features per segment:")
print(segment_means)

## Creates csv table in under customer segmentation
df_final.to_csv("customer_segmentation/customer_segments.csv", index=False)
print("Saved 'customer_segments.csv' with Customer ID & segment name")

