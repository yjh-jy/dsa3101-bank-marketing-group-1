import pandas as pd
import os

def load_data(project_root):
    """
    Load processed customer data CSV files.

    Args:
        project_root (str): Path to the project root directory.

    Returns:
        tuple: A tuple containing:
            - customer_df (pd.DataFrame): DataFrame with customer data.
            - loans_df (pd.DataFrame): DataFrame with loan data.
            - customer_segments_df (pd.DataFrame): DataFrame with customer segmentation data.
            - products_df (pd.DataFrame): DataFrame with product ownership data.
    """
    data_path = os.path.join(project_root, "data", "processed")
    segments_path = os.path.join(project_root, "customer_segmentation")
    # Load the CSV files
    customer_df = pd.read_csv(os.path.join(data_path, "customer.csv"))
    loans_df = pd.read_csv(os.path.join(data_path, "loans.csv"))
    customer_segments_df = pd.read_csv(os.path.join(segments_path, "customer_segments.csv"))
    products_df = pd.read_csv(os.path.join(data_path, "products_owned.csv"))
    return customer_df, loans_df, customer_segments_df, products_df
