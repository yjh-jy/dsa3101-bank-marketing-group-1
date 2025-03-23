import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import chi2_contingency

# Make sure output folders exist
os.makedirs('figures/boxplots', exist_ok=True)
os.makedirs('figures/barplots', exist_ok=True)


def check_missing_correlation(df, col_to_check, target_col):
    # Filter rows where col_to_check is missing
    filtered_df = df[df[col_to_check].isnull()]

    # Print number of missing values
    num_missing = len(filtered_df)
    print(f"Total missing values in '{col_to_check}': {num_missing}")

    # Print value counts of the target column for these rows
    if num_missing > 0:
        print(f"\nValue counts of '{target_col}' where '{col_to_check}' is missing:")
        print(filtered_df[target_col].value_counts(dropna=False))
    else:
        print(f"No missing values in '{col_to_check}'.")

    return filtered_df[target_col].value_counts(dropna=False)

def get_boxplot(df, target_col):
    binary_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <=10 and 
                   df[col].dtype in ['int64', 'float64']]
    num_cols = df.select_dtypes(include=['number']).columns.difference(binary_cols)
    num_cols = [col for col in num_cols if col != target_col]  

    for col in num_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target_col], y=df[col])
        plt.title(f'Boxplot of {col} by {target_col}')
        plt.savefig(f'figures/boxplots/{col}_boxplot.png')
        plt.show()


def get_ttest(df, target_col):
    binary_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <= 10 and 
                   df[col].dtype in ['int64', 'float64']]
    num_cols = df.select_dtypes(include=['number']).columns.difference(binary_cols)
    num_cols = [col for col in num_cols if col != target_col] 

    results = []
    for col in num_cols:
        group1 = df[df[target_col] == 0][col].dropna()
        group2 = df[df[target_col] == 1][col].dropna()
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        results.append({'Feature': col, 'T-Statistic': t_stat, 'P-Value': p_value})

    return pd.DataFrame(results).sort_values(by="P-Value")


def get_proportion_table(df, cat_col, target_col):
    return pd.crosstab(df[cat_col], df[target_col], normalize='index')


def get_chi_square(df, cat_cols, target_col):
    results = []
    
    for col in cat_cols:
        contingency_table = pd.crosstab(df[col], df[target_col])
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        results.append({'Feature': col, 'Chi-Square': chi2, 'P-Value': p})

    return pd.DataFrame(results).sort_values(by="P-Value")


def get_barplot(df, cat_col, target_col):
    plt.figure(figsize=(8, 5))
    sns.barplot(x=df[cat_col], y=df[target_col], estimator=lambda x: sum(x) / len(x))  # Mean proportion of engagement
    plt.title(f'Proportion of {target_col} by {cat_col}')
    plt.ylabel(f'Proportion of {target_col}')
    plt.xlabel(cat_col)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'figures/barplots/{cat_col}_barplot.png')    
    plt.show()