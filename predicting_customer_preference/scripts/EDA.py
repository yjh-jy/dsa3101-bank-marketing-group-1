import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_heatmaps(merged_data, product_columns, save_path):
    """
    Plot and save heatmaps for the relationship between product ownership and active loans.

    Args:
        merged_data (pd.DataFrame): Merged DataFrame that includes a 'has_active_loan' column.
        product_columns (list): List of product ownership column names.
    """
    columns = 3
    rows = math.ceil(len(product_columns) / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(18, rows * 5))
    axes = axes.flatten()

    for i, product in enumerate(product_columns):
        # Create a contingency table for product ownership vs. active loans
        contingency = pd.crosstab(merged_data[product], merged_data['has_active_loan'])
        sns.heatmap(contingency, annot=True, cmap="Blues", fmt="d", ax=axes[i])
        axes[i].set_title(f'Has Active Loans vs {product}')
        axes[i].set_xlabel('Has Active Loans')
        axes[i].set_ylabel('Product Ownership')

    # Hide any unused subplots
    for i in range(len(product_columns), len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    plot_path = os.path.join(save_path, "heatmaps_active_loans.png")
    plt.savefig(plot_path)
    plt.close()

def plot_categorical_features(df, categorical_features, save_path):
    """
    Plot and save bar plots for the distribution of categorical features.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        categorical_features (list): List of categorical column names to plot.
    """
    plt.figure(figsize=(12, 8))
    for i, feature in enumerate(categorical_features, 1):
        plt.subplot(2, 3, i)
        sns.countplot(x=feature, hue=feature, data=df, palette="Set2", legend=False)
        plt.title(f'Distribution of {feature}')
        plt.xticks(rotation=45)
    plt.tight_layout()
    plot_path = os.path.join(save_path, "categorical_features.png")
    plt.savefig(plot_path)
    plt.close()

def plot_correlation_matrix(df, features, save_path):
    """
    Plot and save a heatmap of the correlation matrix for the specified numerical features.

    Args:
        df (pd.DataFrame): DataFrame containing the data.
        features (list): List of feature names for which to compute the correlation matrix.
    """
    correlation_matrix = df[features].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plot_path = os.path.join(save_path, "correlation_matrix.png")
    plt.savefig(plot_path)
    plt.close()

def plot_product_counts(products_df, save_path):
    """
    Plot and save bar charts for the number of customers owning each product 
    and the ownership rates.

    Args:
        products_df (pd.DataFrame): DataFrame with product ownership data (must include a 'customer_id' column).
    """
    # Calculate product counts (excluding customer_id)
    product_counts = products_df.drop(columns=["customer_id"]).sum()
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Bar plot: Number of customers per product
    product_counts.plot(kind="bar", color="skyblue", edgecolor="black", ax=axes[0])
    axes[0].set_title("Number of Customers Owning Each Product")
    axes[0].set_xlabel("Product Type")
    axes[0].set_ylabel("Number of Customers")
    axes[0].tick_params(axis='x', rotation=45)
    
    # Bar plot: Ownership rates for each product
    products_df.drop(columns="customer_id").mean().sort_values().plot(kind="barh", ax=axes[1],
                                                                       color="skyblue", edgecolor="black")
    axes[1].set_title("Ownership Rates of Different Products")
    axes[1].set_xlabel("Proportion of Customers")
    
    plt.tight_layout()
    plot_path = os.path.join(save_path, "product_counts.png")
    plt.savefig(plot_path)
    plt.close()

def drop_unwanted_features(df, features_to_drop):
    """
    Drops specified features from the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame.
        features_to_drop (list): List of column names to drop.

    Returns:
        pd.DataFrame: DataFrame with the specified columns removed.
    """
    return df.drop(columns=features_to_drop)
