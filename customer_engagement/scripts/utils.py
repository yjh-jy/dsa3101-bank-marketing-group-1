"""
utils.py
Helper functions for data loading, EDA, and data quality checks.
"""

import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2_contingency

DATA_DIR = "../../data/processed"
FIGURES_DIR = "../figures"

# =========================
# Data Quality Functions
# =========================

def print_null_summary(df, name="dataframe"):
    """
    Prints the total number and percentage of null values in each column of the given DataFrame,
    sorted by highest null percentage.
    """
    null_counts = df.isnull().sum()
    null_percents = df.isnull().mean() * 100
    summary = pd.DataFrame({
        "Null Count": null_counts,
        "Null %": null_percents.round(2)
    }).sort_values("Null %", ascending=False)
    print(f"\nNull Summary for {name}:\n", summary)

def print_shape_and_preview(df, name="dataframe"):
    """
    Prints the shape (rows, columns) of the DataFrame and displays the first few rows for a quick preview.
    """
    print(f"\n{name} shape: {df.shape}")
    print(f"\n{name} preview:\n{df.head()}")

def check_post_merge_nulls(df, key_cols, name="merged_df"):
    """
    After merging dataframes, prints the percentage of null values in key columns,
    helping to detect any merge-related data loss.
    """
    null_percents = df[key_cols].isnull().mean().round(4) * 100
    print(f"\n{name} - Null % in columns:\n{null_percents.sort_values(ascending=False)}")

def impute_missing_values(df):
    """
    Impute missing values: mode for categorical/low-cardinality columns, median for continuous numeric ones.
    Note: returns a modified copy of the dataframe.
    """
    df = df.copy()
    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype == "object" or df[col].nunique() <= 10:
                mode_val = df[col].mode().iloc[0]
                df[col] = df[col].fillna(mode_val)
            else:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
    return df

# =========================
# Data Loading Functions
# =========================

def load_customer_data():
    '''
    Loads csv files for customer-level engagement analysis
    '''
    engagement_details = pd.read_csv(f"{DATA_DIR}/engagement_details.csv")
    customers = pd.read_csv(f"{DATA_DIR}/customer.csv")
    digital_usage = pd.read_csv(f"{DATA_DIR}/digital_usage.csv")
    products_owned = pd.read_csv(f"{DATA_DIR}/products_owned.csv")
    transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv")
    return engagement_details, customers, digital_usage, products_owned, transactions

def load_campaign_data():
    '''
    Loads csv files for campaign-level engagement analysis
    '''
    engagement_details = pd.read_csv(f"{DATA_DIR}/engagement_details.csv")
    campaigns = pd.read_csv(f"{DATA_DIR}/campaigns.csv")
    return engagement_details, campaigns

# =========================
# EDA Functions
# =========================

# Make sure output folders exist
os.makedirs(f"{FIGURES_DIR}/boxplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/barplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/violinplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/histograms", exist_ok=True)

def get_categorical_columns(df, exclude_col=None, max_unique=10):
    """ 
    Identify categorical columns by by type object or low-cardinality numerical columns
    """
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols += [col for col in df.columns
                 if df[col].dropna().nunique() <= max_unique and
                 df[col].dtype in ["int64", "float64", "int32"] and col != exclude_col]
    if exclude_col in cat_cols:
        cat_cols = cat_cols.drop(exclude_col)
    return list(set(cat_cols))

def get_numerical_columns(df, exclude_col=None, max_unique=10):
    """
    Identify continuous numerical features, excluding categorical-like numerical columns
    """
    cat_cols = get_categorical_columns(df, exclude_col=exclude_col, max_unique=max_unique)
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    if exclude_col in num_cols:
        num_cols = num_cols.drop(exclude_col)
    return list(num_cols)

def plot_numeric_distributions(df, prefix, cols=None):
    """
    Plots histograms with KDE for selected or auto-detected numeric columns.
    Saves plots as f"{FIGURES_DIR}/histograms/<prefix>_colname_hist.png".
    """
    if cols is None:
        num_cols = get_numerical_columns(df)
    else:
        num_cols = cols

    for col in num_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), bins=30, kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(f"{FIGURES_DIR}/histograms/{prefix}_{col}_hist.png")
        plt.close()


def plot_product_ownership_barplot(df, id_col):
    """
    Plots bar chart showing average product ownership proportions.
    Saves the plot as figures/barplots/product_ownership_barplot.png.
    """
    product_cols = [col for col in df.columns if col != id_col]

    df[product_cols].mean().sort_values(ascending=False).plot(kind="bar")
    plt.title("Proportion of Customers Owning Each Product")
    plt.ylabel("Proportion")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/barplots/product_ownership_barplot.png")
    plt.close()


def check_missing_correlation(df, col_to_check, target_col):
    """
    Analyse the relationship between missing values in a column and a target variable.
    """
    # Filter rows where col_to_check is missing
    filtered_df = df[df[col_to_check].isnull()]

    # Print number of missing values
    num_missing = len(filtered_df)
    print(f"Total missing values in \"{col_to_check}\": {num_missing}")

    # Print value counts of the target column for these rows
    if num_missing > 0:
        print(f"\nValue counts of \"{target_col}\" where \"{col_to_check}\" is missing:")
        print(filtered_df[target_col].value_counts(dropna=False))
    else:
        print(f"No missing values in \"{col_to_check}\".")

    return filtered_df[target_col].value_counts(dropna=False)


def get_boxplot(df, target_col):
    """
    Generate and save boxplots of numeric features (excluding categorical-like ones), 
    grouped by a binary target column.
    """
    # Identify continuous numeric columns (exclude categorical-like ones and target column)
    num_cols = get_numerical_columns(df, exclude_col=target_col)

    # Loop through each numeric column to create boxplots
    for col in num_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target_col], y=df[col])
        plt.title(f"Boxplot of {col} by {target_col}")
        plt.savefig(f"{FIGURES_DIR}/boxplots/{col}_boxplot.png")
        plt.close()


def get_ttest(df, target_col):
    """
    Perform Welch's t-test for numeric features against a binary target column.
    """
    # Identify continuous numeric columns (exclude categorical-like ones and target column)
    num_cols = get_numerical_columns(df, exclude_col=target_col)

    results = []
    # Loop through each numeric column
    for col in num_cols:
        # Split into two groups based on target (assumes binary target column with values 0 or 1
        group1 = df[df[target_col] == 0][col].dropna()
        group2 = df[df[target_col] == 1][col].dropna()
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        results.append({"Feature": col, "T-Statistic": t_stat, "P-Value": p_value})

    # Return results sorted by p-value in ascending order
    return pd.DataFrame(results).sort_values(by="P-Value")


def get_proportion_table(df, target_col):
    """
    Print and return normalized crosstab tables for all categorical features 
    vs the target column.
    """
    # Get categorical columns excluding target column
    cat_cols = get_categorical_columns(df, exclude_col=target_col)

    proportion_tables = {}
    # Loop through each categorical column to generate cross-tab
    for col in cat_cols:
        table = pd.crosstab(df[col], df[target_col], normalize="index")
        print(f"\nProportion Table for {col}:")
        print(table)
        proportion_tables[col] = table
    return proportion_tables


def get_chi_square(df, target_col):
    """
    Perform chi-square test of independence between categorical features and the target column.
    """
    # Get categorical columns excluding target column
    cat_cols = get_categorical_columns(df, exclude_col=target_col)

    results = []
    # Loop through each categorical column and create contingency table
    for col in cat_cols:
        contingency_table = pd.crosstab(df[col], df[target_col])
        # Run chi-square test
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        results.append({"Feature": col, "Chi-Square": chi2, "P-Value": p})

    return pd.DataFrame(results).sort_values(by="P-Value")


def get_barplot(df, target_col):
    """
    Generate and save barplots showing the mean proportion of the target variable
    for each level of categorical features.
    """
    # Get categorical columns excluding target column
    cat_cols = get_categorical_columns(df, exclude_col=target_col)

    # Loop through each categorical column and create barplot
    for col in cat_cols:
        plt.figure(figsize=(8, 5))
        sns.barplot(x=df[col], y=df[target_col], estimator=lambda x: sum(x) / len(x)) 
        plt.title(f"Proportion of {target_col} by {col}")
        plt.ylabel(f"Proportion of {target_col}")
        plt.xlabel(col)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{FIGURES_DIR}/barplots/{col}_barplot.png")    
        plt.close()


def get_violin_plots_by_engagement_bin(df, target_col):
    """
    Generate and save violin plots of continuous numeric features across quantile bins 
    of the engagement rate.
    """
    # Identify continuous numeric columns (exclude categorical-like ones and target column)
    num_cols = get_numerical_columns(df, exclude_col=target_col)

    # Bin the engagement rate into 3 equal-sized groups
    df["bin"] = pd.qcut(df[target_col], q=3, labels=["Low", "Medium", "High"])

    # Loop through each numeric column and generate violin plot
    for col in num_cols:
        sns.violinplot(data=df, x="bin", y=col, inner="quartile")
        plt.title(f"{col} by {target_col} Bin")
        plt.xlabel(f"{target_col} Category")
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(f"{FIGURES_DIR}/violinplots/{col}_violinplot.png")
        plt.close()

    df.drop(columns="bin", inplace=True)