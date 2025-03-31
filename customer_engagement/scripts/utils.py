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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# =========================
# Global Constants
# =========================

# Get absolute path to the scripts folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get project root (2 levels up)
PROJECT_ROOT = os.path.abspath(f"{SCRIPT_DIR}/../../")

# Folder path to processed data
DATA_DIR = f"{PROJECT_ROOT}/data/processed"
# Folder path to output figures
FIGURES_DIR = f"{PROJECT_ROOT}/customer_engagement/figures"


# Ensure output folders exist
os.makedirs(f"{FIGURES_DIR}/boxplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/barplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/violinplots", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/histograms", exist_ok=True)
os.makedirs(f"{FIGURES_DIR}/multivariate", exist_ok=True)

# =========================
# Data Quality Functions
# =========================

def print_null_summary(df, name="dataframe"):
    """
    Prints the total number and percentage of null values in each column of the given dataframe,
    sorted by highest null percentage.

    Args:
        df (pd.DataFrame): The dataframe to analyze.
        name (str): Optional name to display in the summary title.
    """
    # Count null values per column
    null_counts = df.isnull().sum()
    # Calculate percentage of nulls per column
    null_percents = df.isnull().mean() * 100
    # Create summary table of null counts and percentages
    summary = pd.DataFrame({
        "Null Count": null_counts,
        "Null %": null_percents.round(2)
    }).sort_values("Null %", ascending=False)
    # Print the summary table
    print(f"\nNull Summary for {name}:\n", summary)


def print_shape_and_preview(df, name="dataframe"):
    """
    Prints the shape (rows, columns) of the dataframe and displays the first few rows for a quick preview.

    Args:
        df (pd.DataFrame): The dataframe to analyze.
        name (str): Optional name to display.
    """
    # Print shape of dataframe
    print(f"\n{name} shape: {df.shape}")
    # Print first 5 rows of dataframe
    print(f"\n{name} preview:\n{df.head()}")


def check_post_merge_nulls(df, key_cols, name="merged_df"):
    """
    After merging dataframes, prints the percentage of null values in key columns,
    helping to detect any merge-related data loss.

    Args:
        df (pd.DataFrame): Merged dataframe.
        key_cols (list): Columns to check for null values.
        name (str): Optional name to display.
    """
    # Calculate null percentages in key columns
    null_percents = df[key_cols].isnull().mean().round(4) * 100
    # Print null percentage summary
    print(f"\n{name} - Null % in columns:\n{null_percents.sort_values(ascending=False)}")


def impute_missing_values(df):
    """
    Impute missing values: mode for categorical/low-cardinality columns, median for continuous numeric ones.
    Returns a modified copy of the dataframe.

    Args:
        df (pd.DataFrame): Dataframe to process.

    Returns:
        pd.DataFrame: Copy of dataframe with imputed values.
    """
    df = df.copy()  # Avoid modifying original dataframe
    # Loop through columns to impute missing values
    for col in df.columns:
        if df[col].isnull().any():
            # Impute categorical or low-cardinality columns with mode
            if df[col].dtype == "object" or df[col].nunique() <= 10:
                mode_val = df[col].mode().iloc[0]
                df[col] = df[col].fillna(mode_val)
            else:
                # Impute continuous numeric columns with median
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
    return df

# =========================
# Data Loading Functions
# =========================

def load_customer_data():
    """
    Loads csv files for customer-level engagement analysis.

    Returns:
        tuple: dataframes for engagement_details, customers, digital_usage, products_owned, transactions.
    """
    # Load customer engagement-related data
    engagement_details = pd.read_csv(f"{DATA_DIR}/engagement_details.csv")
    customers = pd.read_csv(f"{DATA_DIR}/customer.csv")
    digital_usage = pd.read_csv(f"{DATA_DIR}/digital_usage.csv")
    products_owned = pd.read_csv(f"{DATA_DIR}/products_owned.csv")
    transactions = pd.read_csv(f"{DATA_DIR}/transactions.csv")
    return engagement_details, customers, digital_usage, products_owned, transactions


def load_campaign_data():
    """
    Loads csv files for campaign-level engagement analysis.

    Returns:
        tuple: dataframes for engagement_details and campaigns.
    """
    # Load engagement and campaign data
    engagement_details = pd.read_csv(f"{DATA_DIR}/engagement_details.csv")
    campaigns = pd.read_csv(f"{DATA_DIR}/campaigns.csv")
    return engagement_details, campaigns

# =========================
# EDA Functions
# =========================

def get_categorical_columns(df, exclude_col=None, max_unique=10):
    """ 
    Identify categorical columns by type object or low-cardinality numerical columns.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        exclude_col (str): Column to exclude.
        max_unique (int): Max unique values threshold.

    Returns:
        list: List of categorical column names.
    """
    # Select columns of object type
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    # Add numerical columns with low cardinality
    cat_cols += [col for col in df.columns
                 if df[col].dropna().nunique() <= max_unique and
                 df[col].dtype in ["int64", "float64", "int32"] and col != exclude_col]
    # Drop exclude_col if present
    if exclude_col in cat_cols:
        cat_cols = cat_cols.drop(exclude_col)
    return list(set(cat_cols))


def get_numerical_columns(df, exclude_col=None, max_unique=10):
    """
    Identify continuous numerical features, excluding categorical-like numerical columns.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        exclude_col (str): Column to exclude.
        max_unique (int): Max unique values threshold.

    Returns:
        list: List of numerical column names.
    """
    # Get list of categorical columns
    cat_cols = get_categorical_columns(df, exclude_col=exclude_col, max_unique=max_unique)
    # Get numeric columns not in categorical columns
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    # Drop exclude_col if present
    if exclude_col in num_cols:
        num_cols = num_cols.drop(exclude_col)
    return list(num_cols)


def plot_numeric_distributions(df, prefix, cols=None):
    """
    Plots histograms with KDE for selected or auto-detected numeric columns.
    Saves plots in figures/histograms/<prefix>_colname_hist.png.

    Args:
        df (pd.DataFrame): Dataframe to plot.
        prefix (str): Prefix for saved filenames.
        cols (list): Specific columns to plot (optional).
    """
    # Auto-detect numeric columns if cols not provided
    num_cols = get_numerical_columns(df) if cols is None else cols
    # Plot histogram for each numeric column
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
    Saves plot as figures/barplots/product_ownership_barplot.png.

    Args:
        df (pd.DataFrame): Dataframe to plot.
        id_col (str): Column name to exclude.
    """
    # Identify product columns (excluding id_col)
    product_cols = [col for col in df.columns if col != id_col]
    # Plot mean product ownership proportions
    df[product_cols].mean().sort_values(ascending=False).plot(kind="bar")
    plt.title("Proportion of Customers Owning Each Product")
    plt.ylabel("Proportion")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/barplots/product_ownership_barplot.png")
    plt.close()


def check_missing_correlation(df, col_to_check, target_col):
    """
    Analyze the relationship between missing values in a column and a target variable.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        col_to_check (str): Column to check for missing values.
        target_col (str): Target column to analyze correlation.

    Returns:
        pd.Series: Value counts of target column where col_to_check is missing.
    """
    # Filter rows where col_to_check is missing
    filtered_df = df[df[col_to_check].isnull()]
    # Print number of missing values
    num_missing = len(filtered_df)
    print(f"Total missing values in \"{col_to_check}\": {num_missing}")
    # Print target column counts if missing exists
    if num_missing > 0:
        print(f"\nValue counts of \"{target_col}\" where \"{col_to_check}\" is missing:")
        print(filtered_df[target_col].value_counts(dropna=False))
    else:
        print(f"No missing values in \"{col_to_check}\".")
    return filtered_df[target_col].value_counts(dropna=False)


def get_boxplot(df, target_col):
    """
    Generate and save boxplots of numeric features grouped by a binary target column.

    Args:
        df (pd.DataFrame): Dataframe to plot.
        target_col (str): Target column for grouping.
    """
    # Identify numeric columns excluding categorical-like ones and target column
    num_cols = get_numerical_columns(df, exclude_col=target_col)
    # Create boxplot for each numeric column
    for col in num_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target_col], y=df[col])
        plt.title(f"Boxplot of {col} by {target_col}")
        plt.savefig(f"{FIGURES_DIR}/boxplots/{col}_boxplot.png")
        plt.close()


def get_ttest(df, target_col):
    """
    Perform Welch's t-test for numeric features against a binary target column.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        target_col (str): Target column for grouping.

    Returns:
        pd.DataFrame: T-test results.
    """
    # Identify numeric columns
    num_cols = get_numerical_columns(df, exclude_col=target_col)
    results = []
    # Perform t-test for each numeric column
    for col in num_cols:
        # Split column values by binary target groups
        group1 = df[df[target_col] == 0][col].dropna()
        group2 = df[df[target_col] == 1][col].dropna()
        # Conduct Welch's t-test
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
        results.append({"Feature": col, "T-Statistic": t_stat, "P-Value": p_value})
    return pd.DataFrame(results).sort_values(by="P-Value")


def get_proportion_table(df, target_col):
    """
    Print and return normalized crosstab tables for all categorical features vs the target column.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        target_col (str): Target column.

    Returns:
        dict: Crosstab proportion tables.
    """
    # Get categorical columns
    cat_cols = get_categorical_columns(df, exclude_col=target_col)
    proportion_tables = {}
    # Generate crosstab for each categorical column
    for col in cat_cols:
        table = pd.crosstab(df[col], df[target_col], normalize="index")
        print(f"\nProportion Table for {col}:")
        print(table)
        proportion_tables[col] = table
    return proportion_tables


def get_chi_square(df, target_col):
    """
    Perform chi-square test of independence between categorical features and the target column.

    Args:
        df (pd.DataFrame): Dataframe to analyze.
        target_col (str): Target column.

    Returns:
        pd.DataFrame: Chi-square test results.
    """
    # Get categorical columns
    cat_cols = get_categorical_columns(df, exclude_col=target_col)
    results = []
    # Perform chi-square test for each categorical column
    for col in cat_cols:
        # Create contingency table
        contingency_table = pd.crosstab(df[col], df[target_col])
        # Run chi-square test
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        results.append({"Feature": col, "Chi-Square": chi2, "P-Value": p})
    return pd.DataFrame(results).sort_values(by="P-Value")


def get_barplot(df, target_col):
    """
    Generate and save barplots showing the mean proportion of the target variable
    for each level of categorical features.

    Args:
        df (pd.DataFrame): Dataframe to plot.
        target_col (str): Target column.
    """
    # Get categorical columns
    cat_cols = get_categorical_columns(df, exclude_col=target_col)
    # Create barplot for each categorical column
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

    Args:
        df (pd.DataFrame): Dataframe to plot.
        target_col (str): Target column.
    """
    # Identify numeric columns excluding target column
    num_cols = get_numerical_columns(df, exclude_col=target_col)
    # Bin the engagement rate into 3 equal-sized groups
    df["bin"] = pd.qcut(df[target_col], q=3, labels=["Low", "Medium", "High"])
    # Create violin plot for each numeric column
    for col in num_cols:
        sns.violinplot(data=df, x="bin", y=col, inner="quartile")
        plt.title(f"{col} by {target_col} Bin")
        plt.xlabel(f"{target_col} Category")
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(f"{FIGURES_DIR}/violinplots/{col}_violinplot.png")
        plt.close()
    # Remove bin column after plotting
    df.drop(columns="bin", inplace=True)

def run_multivariate_exploration(df, target_col, feature_cols):
    """
    Performs exploratory multivariate analysis using logistic regression and decision tree.

    Args:
        df (dataframe): Cleaned customer-level dataframe.
        target_col (str): Column name of engagement binary target.
        feature_cols (list): List of feature column names to use.

    Returns:
        None
    """
    # Split data
    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Logistic Regression
    logreg = LogisticRegression(max_iter=1000, random_state=42)
    logreg.fit(X_train, y_train)
    print("\nLogistic Regression Classification Report:")
    print(classification_report(y_test, logreg.predict(X_test)))

    coef_df = pd.DataFrame({
        "Feature": feature_cols,
        "Coefficient": logreg.coef_[0]
    }).sort_values(by="Coefficient", key=abs, ascending=False)

    print("\nTop logistic regression coefficients:")
    print(coef_df.head())

    # Decision Tree Feature Importance
    tree = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree.fit(X_train, y_train)
    importances = pd.DataFrame({
        "Feature": feature_cols,
        "Importance": tree.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("\nDecision Tree Feature Importances:")
    print(importances.head())

    # Plot feature importances
    plt.figure(figsize=(10, 5))
    sns.barplot(x="Importance", y="Feature", data=importances.head(10))
    plt.title("Top Decision Tree Feature Importances")
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/multivariate/feature_importances.png")
    plt.close()