# Customer segmentation into 3 categories ("High-value", "At risk / inactive customers", "Budget-conscious")
## Importing packages
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from scipy.stats.mstats import winsorize
from scipy.stats import zscore
import os


## READING IN DATA
project_root = os.getcwd()  # Assumes script runs from project root
# Define the path to the processed data folder
data_path = os.path.join(project_root, "data", "processed")
# Load the CSV files
customer_df = pd.read_csv(os.path.join(data_path, "customer.csv"))
digital_usage_df = pd.read_csv(os.path.join(data_path, "digital_usage.csv"))
transactions_df = pd.read_csv(os.path.join(data_path, "transactions.csv"))
products_df = pd.read_csv(os.path.join(data_path, "products_owned.csv"))

# Ensure transaction dates are in datetime format
transactions_df["transaction_date"] = pd.to_datetime(transactions_df["transaction_date"])

# Days from last transaction
latest_transaction = transactions_df.groupby("customer_id")["transaction_date"].max().reset_index()
latest_transaction["transaction_date"] = pd.to_datetime(latest_transaction["transaction_date"]) 
reference_date = pd.to_datetime("2025-01-01")
latest_transaction["days_from_last_transaction"] = (reference_date - latest_transaction["transaction_date"]).dt.days
latest_transaction = latest_transaction[["customer_id", "days_from_last_transaction"]]
### Calculate avg_transaction_amt per customer
transaction_summary = transactions_df.groupby("customer_id").agg(total_transaction_amt=("transaction_amt", "sum"),num_transactions=("transaction_id", "count")).reset_index()
transaction_summary["avg_transaction_amt"] = transaction_summary["total_transaction_amt"] / transaction_summary["num_transactions"]
transaction_summary["avg_transaction_amt"] = transaction_summary["avg_transaction_amt"].replace([np.inf, -np.inf], 0).fillna(0)
transaction_summary = transaction_summary[["customer_id", "avg_transaction_amt", "num_transactions"]]


### Calculate digital engagement score
scaler = MinMaxScaler() 
digital_usage_df["normalized_logins"] = scaler.fit_transform(digital_usage_df[["mobile_logins_wk", "web_logins_wk"]].sum(axis=1).values.reshape(-1, 1))
digital_usage_df["normalized_session_time"] = scaler.fit_transform(digital_usage_df[["avg_mobile_time", "avg_web_time"]].sum(axis=1).values.reshape(-1, 1))
digital_usage_df["digital_engagement_score"] = (digital_usage_df["normalized_logins"] * 0.7 +digital_usage_df["normalized_session_time"] * 0.3)
### Correct aggregation step
digital_engagement = digital_usage_df.groupby("customer_id", as_index=False)["digital_engagement_score"].mean()

### Total products owned
products_df["total_products_owned"] = products_df.iloc[:, 1:].sum(axis=1)
products_summary = products_df[["customer_id", "total_products_owned"]]

## Extracting relevant columns from customer table
customer_features = ['customer_id', 'income', 'balance', 'customer_lifetime_value', 'debt', 'tenure', 'default']
customer_subset_df = customer_df[customer_features]

## MERGE DATASETS
df = customer_subset_df.merge(latest_transaction, on="customer_id", how="left")
df = df.merge(transaction_summary[["customer_id", "avg_transaction_amt", "num_transactions"]], on="customer_id", how="left")
df = df.merge(digital_engagement[["customer_id", "digital_engagement_score"]], on="customer_id", how="left")
df = df.merge(products_df[["customer_id", "total_products_owned"]], on="customer_id", how="left")
# Insert another interaction term (transaction freq)
# Since data only avail from 2023-2024, transactions before 2023 for those with tenure >24 months not consider
df["effective_tenure"] = df["tenure"].clip(upper=24)
df["transaction_freq"] = df["num_transactions"] / df["effective_tenure"]
df["transaction_freq"] = df["transaction_freq"].replace([np.inf, -np.inf], 0).fillna(0)
df.drop(columns=["effective_tenure"], inplace=True)

print(df.isnull().sum())

## HANDLING MISSING VALUES
### engagement score only has 19 missing values -> fill with mean
df["digital_engagement_score"].fillna(df["digital_engagement_score"].mean(), inplace=True)
### no transaction record (we set transactions to be 0)
df["avg_transaction_amt"].fillna(0, inplace=True)
df["transaction_freq"].fillna(0, inplace=True)
df["num_transactions"].fillna(0, inplace=True)
### some did not do transactions. we set the days from last transaction to be a high but not too extreme value. We add a months of buffer
df["days_from_last_transaction"].fillna(df["days_from_last_transaction"].max() + 30, inplace=True)

print(df.isnull().sum())

features_to_scale = [ "income", "balance", "debt", "customer_lifetime_value","days_from_last_transaction", "avg_transaction_amt","digital_engagement_score", "total_products_owned", "transaction_freq"]
# Check for outliers
# Create 3x3 grid
project_root = os.getcwd()
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 12))
fig.suptitle("Feature-Wise Outlier Visualization", fontsize=16)
axes = axes.flatten()
# Make visuals folder
visuals_path = os.path.join(project_root, "customer_segmentation", "visuals")
os.makedirs(visuals_path, exist_ok=True)
# Plot boxplots
for i, feature in enumerate(features_to_scale):
    sns.boxplot(y=df[feature], ax=axes[i])
    axes[i].set_title(feature)
    axes[i].set_ylabel("") 
    axes[i].grid(True)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plot_path = os.path.join(visuals_path, "boxplots_for_outliers.png")
plt.savefig(plot_path)


# Define function to count outliers using Z-score method
def count_outliers_zscore(df, threshold=3):
    outlier_counts = {}

    for col in df.select_dtypes(include=[np.number]): 
        z_scores = np.abs(zscore(df[col])) 
        num_outliers = (z_scores > threshold).sum()
        outlier_counts[col] = num_outliers

    return pd.DataFrame.from_dict(outlier_counts, orient="index", columns=["Outlier Count"])

# Apply to dataset
outliers_zscore_df = count_outliers_zscore(df)
print(outliers_zscore_df)


## STANDARDIZING FOR K-MEANS CLUSTERING
# Features that need Robust scaling 
# Features that need Robust scaling 
robust_features = ["income", "balance", "debt", "customer_lifetime_value",  "avg_transaction_amt", "transaction_freq"]
# Heavily skewed → higher winsorization
heavy_outliers = ["income", "balance", "debt"]
for col in heavy_outliers:
    df[col] = pd.Series(winsorize(df[col].to_numpy(), limits=[0.05, 0.1])).astype(float)
# Moderate outliers → light winsorization
moderate_outliers = ["customer_lifetime_value", "avg_transaction_amt", "transaction_freq"]
for col in moderate_outliers:
    df[col] = pd.Series(winsorize(df[col].to_numpy(), limits=[0.0, 0.01])).astype(float)


# Features that need Standard scaling (normally distributed)
standard_features = ["days_from_last_transaction", "digital_engagement_score", "total_products_owned"]
# Apply RobustScaler
scalerrobust =  RobustScaler()
df_scaled = df.copy()
df_scaled[robust_features] = scalerrobust.fit_transform(df[robust_features])
# Apply StandardScaler
scaler_standard = StandardScaler()
df_scaled[standard_features] = scaler_standard.fit_transform(df[standard_features])

# boxplot after winsorize
# Create 3x3 grid
fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(15, 12))
fig.suptitle("Feature-Wise Outlier Visualization Post Winsorization", fontsize=16)
axes = axes.flatten()
os.makedirs(visuals_path, exist_ok=True)
# Plot boxplots
for i, feature in enumerate(features_to_scale):
    sns.boxplot(y=df[feature], ax=axes[i])
    axes[i].set_title(feature)
    axes[i].set_ylabel("")  
    axes[i].grid(True)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plot_path = os.path.join(visuals_path, "post_winsorize_boxplots_for_outliers.png")
plt.savefig(plot_path)
plt.close()

# Apply PCA
pca = PCA(n_components=len(features_to_scale))  # Keep all components
df_pca = pca.fit_transform(df_scaled[features_to_scale])

# Convert to DataFrame
explained_variance = pd.DataFrame(
    pca.explained_variance_ratio_,
    index=features_to_scale,
    columns=["Explained Variance"]
)

# Print explained variance of each feature
print("\nPCA Explained Variance:\n", explained_variance.sort_values(by="Explained Variance", ascending=False))


## K-MEANS CLUSTERING
optimal_k = 3
df_scaled["Cluster"] = KMeans(n_clusters= optimal_k,  init="k-means++", n_init=20, random_state=42).fit_predict(df_scaled[features_to_scale])
df["Cluster"] = df_scaled["Cluster"]

# Silhouette Score
silhouette_avg = silhouette_score(df_scaled[features_to_scale], df["Cluster"])
print(f"Silhouette Score = {silhouette_avg:.4f}")

### Number of clients in each cluster
print(df["Cluster"].value_counts())

### Get information about each cluster
cluster_means = df_scaled.groupby("Cluster")[features_to_scale].mean()
print(cluster_means)


cluster_means["score"] = (
    cluster_means["balance"] * 0.2 + 
    cluster_means["debt"] * (-0.05) +  # Negative weight for financial distress
    cluster_means["customer_lifetime_value"] * 0.15 +  # Increased because CLV predicts revenue
    cluster_means["days_from_last_transaction"] * (-0.20) +  # Increased penalty for inactivity
    cluster_means["avg_transaction_amt"] * 0.20 +  # High-value customers spend more per transaction
    cluster_means["digital_engagement_score"] * 0.20 +  # More engagement means higher retention
    cluster_means["total_products_owned"] * 0.20 +  # Owning more products = stronger banking relationship
    cluster_means["transaction_freq"] * 0.20  # Higher impact because frequent usage matters
)

# Rank Clusters Based on Score (Descending)
sorted_clusters = cluster_means["score"].sort_values(ascending=False).index.tolist()

# Assign Segments Based on Rank
dynamic_segment_mapping = {
    sorted_clusters[0]: "High-value",
    sorted_clusters[1]: "Budget-conscious",
    sorted_clusters[2]: "At risk / inactive customers"
}


# Print cluster rankings before applying
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
project_root = os.getcwd() 
df_final.to_csv(os.path.join(project_root, "customer_segmentation", "customer_segments.csv"), index=False)
print("Saved 'customer_segments.csv' with Customer ID & segment name")


# Check if correct Packages installed

required_packages = {
    "pandas": "2.2.3",
    "numpy": "1.23.1",
    "scikit-learn": "1.2.2",
    "matplotlib": "3.10.1",
    "matplotlib-inline": "0.1.6",
    "seaborn": "0.13.2",
    "python-dateutil": "2.9.0.post0",
    "scipy": "1.9.0"
}

mismatched = []

for pkg, required_version in required_packages.items():
    try:
        # Use pip show to get version
        version_info = os.popen(f"pip show {pkg}").read()
        installed_version = None
        for line in version_info.splitlines():
            if line.startswith("Version:"):
                installed_version = line.split(":")[1].strip()
                break
        if not installed_version:
            print(f"Package not installed: {pkg}")
            mismatched.append(f"{pkg}=={required_version}")
        elif installed_version != required_version:
            print(f"Package mismatch: {pkg} - required: {required_version}, installed: {installed_version}")
            mismatched.append(f"{pkg}=={required_version}")
    except Exception as e:
        print(f"Error checking package {pkg}: {e}")
        mismatched.append(f"{pkg}=={required_version}")

if mismatched:
    print("\nThere are mismatches in the package version used and the package versions required. Required packages are stated in the Readme file. To fix the packages, run:")
    print(" pip install pandas==2.2.3 numpy==1.23.1 scikit-learn==1.2.2 matplotlib==3.10.1 matplotlib-inline==0.1.6 seaborn==0.13.2 python-dateutil==2.9.0.post0 scipy==1.9.0")
    print(" in terminal")
