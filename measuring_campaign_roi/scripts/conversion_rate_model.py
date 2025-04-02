import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_predict, KFold


def train_conversion_rate_model(X, y, categorical_features):
    """
    Trains a linear regression model to predict conversion rates using categorical features only.

    Parameters:
    - X (DataFrame): Feature matrix with only categorical columns
    - y (Series or array): Conversion rate target
    - categorical_features (list of str): List of categorical columns to be one-hot encoded

    Returns:
    - model (Pipeline): Trained sklearn pipeline
    - preds (np.ndarray): Cross-validated predicted conversion rates
    - y (Series or array): Ground truth conversion rates
    - coef_df (DataFrame): Table of one-hot encoded feature coefficients
    """

    # One-hot encode categorical features
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ])

    # Pipeline with linear regression
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # 5-fold cross-validation for predictions
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    model.fit(X, y)
    preds = cross_val_predict(model, X, y, cv=kf)

    # Extract model coefficients
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
    coefficients = model.named_steps['regressor'].coef_

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients
    }).sort_values(by='Coefficient', key=abs, ascending=False)

    return model, preds, y, coef_df
