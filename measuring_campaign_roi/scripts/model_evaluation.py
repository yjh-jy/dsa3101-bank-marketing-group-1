import numpy as np
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict

def evaluate_model_performance(preds, true_vals, num_features):
    """
    Computes standard regression metrics: MSE, RMSE, R², and Adjusted R².

    Parameters:
    - preds (array-like): Predicted values
    - true_vals (array-like): Ground truth values
    - num_features (int): Number of model features used (for Adjusted R²)

    Returns:
    - dict: A dictionary containing MSE, RMSE, R2, and Adjusted R2
    """
    n = len(true_vals)
    mse = mean_squared_error(true_vals, preds)
    rmse = (mse)**0.5
    r2 = r2_score(true_vals, preds)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - num_features - 1)

    return {
        "MSE": round(mse,2),
        "RMSE": round(rmse,2),
        "R2": round(r2,2),
        "Adjusted R2": round(adj_r2,2)
    }