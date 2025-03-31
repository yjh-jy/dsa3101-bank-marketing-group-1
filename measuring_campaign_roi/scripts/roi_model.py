import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def train_roi_model(preds_conv, preds_cost, y_roi_train):
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
    model.fit(X_roi_scaled, y_roi_train)

    return model, X_roi_scaled, scaler

def predict_roi_model(model, scaler, X_conv_test, X_cost_test):
    """
    Predicts ROI using the trained model and scaler.

    Parameters:
    - model (LinearRegression): Trained linear regression model
    - scaler (StandardScaler): Scaler used for feature standardization
    - X_conv_test (array-like): Predicted conversion rates for test set
    - X_cost_test (array-like): Predicted acquisition costs for test set

    Returns:
    - preds (ndarray): Predicted ROI values
    """
    X_roi_test = np.column_stack([X_conv_test, X_cost_test])
    X_roi_scaled_test = scaler.transform(X_roi_test)

    preds = model.predict(X_roi_scaled_test)
    return preds