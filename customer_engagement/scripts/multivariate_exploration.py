"""
This script performs multivariate exploratory analysis to complement the univariate and bivariate EDA conducted.

The goal is not to build a predictive model, but to explore how multiple behavioural and financial variables jointly relate to customer engagement.

Specifically, it applies:
- Logistic Regression: to examine the relative contribution of each feature to engagement likelihood.
- Decision Tree Feature Importance: to assess which variables best split engaged vs non-engaged customers.

This multivariate exploration provides an additional layer of insight beyond individual variable associations, supporting the identification of meaningful behavioural patterns.
"""

import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Get absolute path to the scripts folder
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get project root (2 levels up)
PROJECT_ROOT = os.path.abspath(f"{SCRIPT_DIR}/../../")

# Folder path to output figures
FIGURES_DIR = f"{PROJECT_ROOT}/customer_engagement/figures"

# Ensure output folders exist
os.makedirs(f"{FIGURES_DIR}/multivariate", exist_ok=True)

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
    logreg = LogisticRegression(max_iter=1000)
    logreg.fit(X_train, y_train)
    print("\nLogistic Regression Classification Report:")
    print(classification_report(y_test, logreg.predict(X_test)))

    coef_df = pd.DataFrame({
        'Feature': feature_cols,
        'Coefficient': logreg.coef_[0]
    }).sort_values(by='Coefficient', key=abs, ascending=False)

    print("\nTop logistic regression coefficients:")
    print(coef_df.head())

    # Decision Tree Feature Importance
    tree = DecisionTreeClassifier(max_depth=4, random_state=42)
    tree.fit(X_train, y_train)
    importances = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': tree.feature_importances_
    }).sort_values(by='Importance', ascending=False)

    print("\nDecision Tree Feature Importances:")
    print(importances.head())

    # Plot feature importances
    plt.figure(figsize=(10, 5))
    sns.barplot(x='Importance', y='Feature', data=importances.head(10))
    plt.title('Top Decision Tree Feature Importances')
    plt.tight_layout()
    plt.savefig(f"{FIGURES_DIR}/multivariate/feature_importances.png")
    plt.close()
