import pandas as pd

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
