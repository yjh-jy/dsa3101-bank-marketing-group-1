import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import cross_val_predict, KFold

def train_acquisition_cost_model(X, y, categorical_features, numerical_features):
    """
    Trains a linear regression model to predict log-transformed acquisition cost.

    Parameters:
    - X (DataFrame): Feature matrix
    - y (Series): Target variable (log acquisition cost)
    - categorical_features (list of str): Categorical columns to be one-hot encoded
    - numerical_features (list of str): Numerical columns to be passed through

    Returns:
    - model (Pipeline): Trained sklearn pipeline
    - preds (np.ndarray): Predicted acquisition costs (converted back from log scale)
    - true_vals (np.ndarray): Actual acquisition costs (converted back from log scale)
    - coef_df (DataFrame): Coefficient table with feature importance
    """

    # Define preprocessing steps
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ])

    # Create pipeline
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Fit model using 5-fold cross-validation
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    model.fit(X, y)

    log_preds = cross_val_predict(model, X, y, cv=kf)
    preds = np.expm1(log_preds)  # convert back from log scale
    true_vals = np.expm1(y)

    # Extract and interpret coefficients
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
    log_coefs = model.named_steps['regressor'].coef_
    percent_impact = (np.exp(log_coefs) - 1) * 100

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Log Coefficient': log_coefs,
        'Approx % Change in Cost': percent_impact
    }).sort_values(by='Approx % Change in Cost', ascending=False)

    return model, preds, true_vals, coef_df