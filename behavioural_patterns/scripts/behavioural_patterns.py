# Key insights and targeted marketing approaches are in the behavioural_patterns.md file

# Importing packages
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from utils import (
    load_data,
    prepare_data,
    categorize_loan_purpose,
    classify_money_flow
)
from analysis_functions import (
    analyze_nps,
    analyze_financial_health,
    analyze_product_usage,
    analyze_transactions,
    analyze_digital_engagement
)

def main():
    """
    Main function to execute data loading, preparation, and analysis.
    """
    # Load datasets
    customers, digital_usage, loans, products, transactions, segments = load_data()
    
    # Prepare and merge datasets
    df = prepare_data(customers, digital_usage, loans, products, transactions, segments)
    
    # Analyze NPS across customer segments
    analyze_nps(df)
    
    # Analyze financial health across customer segments
    analyze_financial_health(df)
    
    # Analyze product usage across customer segments
    analyze_product_usage(df)
    
    # Analyze transaction history across customer segments
    analyze_transactions(df)
    
    # Analyze digital engagement across customer segments
    analyze_digital_engagement(df)

if __name__ == '__main__':
    main()