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


def check_missing_correlation(df, col_to_check, target_col):
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
    cat_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <=5 and 
                   df[col].dtype in ["int64", "float64"]]
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    num_cols = [col for col in num_cols if col != target_col]  

    for col in num_cols:
        plt.figure(figsize=(8, 5))
        sns.boxplot(x=df[target_col], y=df[col])
        plt.title(f"Boxplot of {col} by {target_col}")
        plt.savefig(f"figures/boxplots/{col}_boxplot.png")
        plt.close()


def get_ttest(df, target_col):
    cat_cols = [col for col in df.columns
                   if df[col].dropna().nunique() <= 5 and 
                   df[col].dtype in ["int64", "float64"]]
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    num_cols = [col for col in num_cols if col != target_col] 

    results = []
    for col in num_cols:
        group1 = df[df[target_col] == 0][col].dropna()
        group2 = df[df[target_col] == 1][col].dropna()
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)

        results.append({"Feature": col, "T-Statistic": t_stat, "P-Value": p_value})

    return pd.DataFrame(results).sort_values(by="P-Value")


def get_proportion_table(df, target_col):
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 10 and 
             df[col].dtype in ["int64", "float64"] and col != target_col]
    cat_cols = list(set(cat_cols) - {target_col})

    proportion_tables = {}
    for col in cat_cols:
        table = pd.crosstab(df[col], df[target_col], normalize="index")
        print(f"\nProportion Table for {col}:")
        print(table)
        proportion_tables[col] = table
    return proportion_tables


def get_chi_square(df, target_col):
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols += [col for col in df.columns 
                 if df[col].dropna().nunique() <= 10 and
                 df[col].dtype in ["int64", "float64"] and col != target_col]
    cat_cols = list(set(cat_cols) - {target_col})
    results = []
    
    for col in cat_cols:
        contingency_table = pd.crosstab(df[col], df[target_col])
        chi2, p, dof, expected = chi2_contingency(contingency_table)

        results.append({"Feature": col, "Chi-Square": chi2, "P-Value": p})

    return pd.DataFrame(results).sort_values(by="P-Value")


def get_barplot(df, target_col):
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    cat_cols += [col for col in df.columns 
             if df[col].dropna().nunique() <= 10 and 
             df[col].dtype in ["int64", "float64"] and col != target_col]
    cat_cols = list(set(cat_cols) - {target_col})

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
    cat_cols = [col for col in df.columns
                if df[col].dropna().nunique() <= 5 and 
                df[col].dtype in ["int64", "float64"]]
    num_cols = df.select_dtypes(include=["number"]).columns.difference(cat_cols)
    num_cols = [col for col in num_cols if col != target_col] 

    df["bin"] = pd.qcut(df[target_col], q=3, labels=["Low", "Medium", "High"])

    for col in num_cols:
        sns.violinplot(data=df, x="bin", y=col, inner="quartile")
        plt.title(f"{col} by {target_col} Bin")
        plt.xlabel(f"{target_col} Category")
        plt.ylabel(col)
        plt.tight_layout()
        plt.savefig(f"figures/violinplots/{col}_violinplot.png")
        plt.close()

    df.drop(columns="bin", inplace=True)