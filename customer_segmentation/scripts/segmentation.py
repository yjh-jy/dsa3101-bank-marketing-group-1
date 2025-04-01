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
from utils import (
    load_data,
    preprocess_data,
    merge_data,
    handle_missing_val,
    save_boxplot,
    count_outliers_zscore,
    handling_outliers,
    feature_scaling,
    pca_explanined_variance,
    KMeans_model,
    label_cluster,
    save_segmentation_csv,
    check_packages
)
import os

def main():
    project_root = os.getcwd() # Check directory ends with dsa3101-bank-marketing-group-1
    customer_df, digital_usage_df, transactions_df, products_df = load_data(project_root)
    customer_subset_df, latest_transaction, transaction_summary, digital_engagement, products_df = preprocess_data(customer_df, digital_usage_df, transactions_df, products_df)
    df = merge_data(customer_subset_df, latest_transaction, transaction_summary, digital_engagement, products_df)
    print(df.isnull().sum())
    df = handle_missing_val(df)
    print(df.isnull().sum())
    features_to_scale = [ "income", "balance", "debt", "customer_lifetime_value","days_from_last_transaction", "avg_transaction_amt","digital_engagement_score", "total_products_owned", "transaction_freq"]
    # Make visuals folder
    visuals_path = os.path.join(project_root, "visuals")
    save_boxplot(df, features_to_scale,  "boxplots_for_outliers.png", visuals_path)
    outliers_zscore_df = count_outliers_zscore(df)
    print(outliers_zscore_df)
    ## STANDARDIZING FOR K-MEANS CLUSTERING
    # Features that need Robust scaling 
    robust_features = ["income", "balance", "debt", "customer_lifetime_value",  "avg_transaction_amt", "transaction_freq"]
    # Heavily skewed → higher winsorization
    heavy_outliers = ["income", "balance", "debt"]
    # Moderate outliers → light winsorization
    moderate_outliers = ["customer_lifetime_value", "avg_transaction_amt", "transaction_freq"]
    df= handling_outliers(df,heavy_outliers, moderate_outliers)
    standard_features = ["days_from_last_transaction", "digital_engagement_score", "total_products_owned"]
    df_scaled = feature_scaling(df, robust_features, standard_features)
    save_boxplot(df, features_to_scale,  "post_winsorize_boxplots_for_outliers.png", visuals_path)
    plt.close()
    pca_explanined_variance(df_scaled, features_to_scale)
    df, df_scaled = KMeans_model(df, df_scaled, features_to_scale, optimal_k=3)
    # Silhouette Score
    silhouette_avg = silhouette_score(df_scaled[features_to_scale], df["Cluster"])
    print(f"Silhouette Score = {silhouette_avg:.4f}")

    ### Number of clients in each cluster
    print(df["Cluster"].value_counts())

    ### Get information about each cluster
    cluster_means = df_scaled.groupby("Cluster")[features_to_scale].mean()
    print(cluster_means)

    weights = {
    "income": 0.1,
    "balance": 0.1,
    "debt": -0.05,
    "customer_lifetime_value": 0.15,
    "days_from_last_transaction": -0.20,
    "avg_transaction_amt": 0.20,
    "digital_engagement_score": 0.20,
    "total_products_owned": 0.20,
    "transaction_freq": 0.20
    }


    df =label_cluster(df, cluster_means, weights)
    print(df["Segment"].value_counts())

    df_final = df[["customer_id", "Segment"]]

    print(df_final.head())

    segment_means = df.groupby("Segment")[features_to_scale].mean()

    # Display the results
    print("Mean of original features per segment:")
    print(segment_means)
    check_packages()
    save_segmentation_csv(df_final)


if __name__ == "__main__":
    main()
