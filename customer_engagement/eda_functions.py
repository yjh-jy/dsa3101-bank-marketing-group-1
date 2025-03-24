import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2_contingency

# Make sure output folders exist
os.makedirs("figures/boxplots", exist_ok=True)
os.makedirs("figures/barplots", exist_ok=True)
os.makedirs("figures/violinplots", exist_ok=True)
os.makedirs("figures/histograms", exist_ok=True)


def check_missing_correlation(df, col_to_check, target_col):
    """
    Analyze the relationship between missing values in a column and a target variable.
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

    # Identify numeric columns with <= 5 unique values: treat as categorical-like
    cat_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <=5 and 
                   df[col].dtype in ["int64", "float64"]]
    # Identify continuous numeric columns (exclude categorical-like ones)
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    # Remove the target column from plotting
    num_cols = [col for col in num_cols if col != target_col]  

    # Loop through each numeric column to create boxplots
    for col in num_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target_col], y=df[col])
        plt.title(f"Boxplot of {col} by {target_col}")
        plt.savefig(f"figures/boxplots/{col}_boxplot.png")
        plt.close()


def get_ttest(df, target_col):
    """
    Perform Welch's t-test for numeric features against a binary target column.
    """

    # Identify numeric columns with <= 5 unique values: treat as categorical-like
    cat_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <=5 and 
                   df[col].dtype in ["int64", "float64"]]
    # Identify continuous numeric columns (exclude categorical-like ones)
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    # Remove the target column from plotting
    num_cols = [col for col in num_cols if col != target_col]  

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

    # Get object (str) columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    # Add numeric columns with <=5 unique values (treat as categorical)
    cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 5 and 
             df[col].dtype in ["int64", "float64"] and col != target_col]
    # Ensure no duplicates and remove the target column
    cat_cols = list(set(cat_cols) - {target_col})

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
    
    # Get object (str) columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    # Add numeric columns with <=5 unique values (treat as categorical)
    cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 5 and 
             df[col].dtype in ["int64", "float64"] and col != target_col]
    # Ensure no duplicates and remove the target column
    cat_cols = list(set(cat_cols) - {target_col})

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

    # Get object (str) columns
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    # Add numeric columns with <=5 unique values (treat as categorical)
    cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 5 and 
             df[col].dtype in ["int64", "float64"] and col != target_col]
    # Ensure no duplicates and remove the target column
    cat_cols = list(set(cat_cols) - {target_col})

    # Loop through each categorical column and create barplot
    for col in cat_cols:
        plt.figure(figsize=(8, 5))
        sns.barplot(x=df[col], y=df[target_col], estimator=lambda x: sum(x) / len(x)) 
        plt.title(f"Proportion of {target_col} by {col}")
        plt.ylabel(f"Proportion of {target_col}")
        plt.xlabel(col)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"figures/barplots/{col}_barplot.png")    
        plt.close()


def get_violin_plots_by_engagement_bin(df, target_col):
    """
    Generate and save violin plots of continuous numeric features across quantile bins 
    of the engagement rate.
    """

    # Identify numeric columns with <= 5 unique values: treat as categorical-like
    cat_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <=5 and 
                   df[col].dtype in ["int64", "float64"]]
    # Identify continuous numeric columns (exclude categorical-like ones)
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    # Remove the target column from plotting
    num_cols = [col for col in num_cols if col != target_col] 

    # Bin the engagement rate into 3 equal-sized groups
    df["bin"] = pd.qcut(df[target_col], q=3, labels=["Low", "Medium", "High"])

    # Loop through each numeric column and generate violin plot
    for col in num_cols:
        sns.violinplot(data=df, x="bin", y=col, inner="quartile")
        plt.title(f"{col} by {target_col} Bin")
        plt.xlabel(f"{target_col} Category")
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(f"figures/violinplots/{col}_violinplot.png")
        plt.close()

    df.drop(columns="bin", inplace=True)

def plot_numeric_distributions(df, prefix, cols=None):
    """
    Plots histograms with KDE for selected or auto-detected numeric columns.
    Saves plots in figures/histograms/<prefix>_colname_hist.png.
    """
    if cols is None:
        cat_cols = [col for col in df.columns
                    if df[col].dropna().nunique() <= 5 and 
                    df[col].dtype in ["int64", "float64"]]
        num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    else:
        num_cols = cols

    for col in num_cols:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[col].dropna(), bins=30, kde=True)
        plt.title(f"Distribution of {col}")
        plt.tight_layout()
        plt.savefig(f"figures/histograms/{prefix}_{col}_hist.png")
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
    plt.savefig("figures/barplots/product_ownership_barplot.png")
    plt.close()