import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def train_roi_model(preds_conv, preds_cost, y_roi):
    """
    Trains a linear regression model to predict ROI using predicted conversion rate
    and predicted acquisition cost as inputs. Standardizes features before training.

    Parameters:
    - preds_conv (array-like): Predicted conversion rates
    - preds_cost (array-like): Predicted acquisition costs
    - y_roi (array-like): Actual ROI values

    Returns:
    - model (LinearRegression): Trained linear regression model
    - X_roi_scaled (ndarray): Scaled input features used in training
    - scaler (StandardScaler): Scaler used for feature standardization
    """
    X_roi = np.column_stack([preds_conv, preds_cost])

    # Standardize features
    scaler = StandardScaler()
    X_roi_scaled = scaler.fit_transform(X_roi)

    # Train linear regression model
    model = LinearRegression()
    model.fit(X_roi_scaled, y_roi)

    return model, X_roi_scaled, scaler