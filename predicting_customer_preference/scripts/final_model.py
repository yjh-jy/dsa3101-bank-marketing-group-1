import pandas as pd

def predict_with_best_model(df, feature_cols, best_models):
    """
    Predict binary labels for each target using the best trained models.

    Args:
        df (pd.DataFrame): The test DataFrame.
        feature_cols (list): List of feature column names used during training.
        best_models (dict): Dictionary containing, for each target, the best model, its preprocessor, and threshold.

    Returns:
        pd.DataFrame: DataFrame containing the customer_id and predictions for each target.
    """
    predictions = {"customer_id": df["customer_id"]}
    
    # Loop through each target and generate predictions
    for target, components in best_models.items():
        X = df[feature_cols]
        preprocessor = components['preprocessor']
        model = components['model']
        threshold = components['threshold']
        
        # Transform features using the preprocessor
        X_processed = preprocessor.transform(X)
        # Get predicted probabilities for the positive class
        y_pred_proba = model.predict_proba(X_processed)[:, 1]
        # Convert probabilities to binary predictions based on threshold
        predictions[target] = (y_pred_proba > threshold).astype(int)
    
    return pd.DataFrame(predictions)