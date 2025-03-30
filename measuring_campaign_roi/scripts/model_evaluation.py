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
    rmse = np.sqrt(mse)
    r2 = r2_score(true_vals, preds)
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - num_features - 1)

    return {
        "MSE": mse,
        "RMSE": rmse,
        "R2": r2,
        "Adjusted R2": adj_r2
    }


def evaluate_roi_model(preds_conv, preds_cost, y_roi, cv=3):
    """
    Evaluates an ROI regression model using predicted conversion rate and cost.
    Applies k-fold CV to estimate R², MSE, and RMSE.

    Parameters:
    - preds_conv (array-like): Predicted conversion rates
    - preds_cost (array-like): Predicted acquisition costs
    - y_roi (array-like): Actual ROI values
    - cv (int): Number of cross-validation folds (default = 3)

    Returns:
    - mean_r2 (float): Mean R² across folds
    - mean_mse (float): Mean MSE across folds
    - mean_rmse (float): Mean RMSE across folds
    """
    X_roi = np.column_stack([preds_conv, preds_cost])
    model = LinearRegression()

    cv_scores_r2 = cross_val_score(model, X_roi, y_roi, cv=cv, scoring='r2')
    mean_r2 = np.mean(cv_scores_r2)

    preds = cross_val_predict(model, X_roi, y_roi, cv=cv)
    mean_mse = mean_squared_error(y_roi, preds)
    mean_rmse = np.sqrt(mean_mse)

    return mean_r2, mean_mse, mean_rmse
