from sklearn.metrics import accuracy_score, recall_score, f1_score
import pandas as pd


def evaluate_model_on_test(predictions_df, df_test, target_cols):
    """
    Evaluate the trained best models on the test dataset by computing accuracy, recall, and F1 scores.

    Args:
        predictions_df (pd.DataFrame): DataFrame containing the predictions for each target.
        df_test (pd.DataFrame): Test dataset containing the true target labels.
        target_cols (list): List of target column names (binary classification).

    Returns:
        dict: A dictionary where each key is a target and the corresponding value is 
              another dictionary with keys 'accuracy', 'recall', and 'f1' representing 
              the respective performance scores on the test data.
    """
    performance_dict = []

    for target in target_cols:
        accuracy = accuracy_score(df_test[target], predictions_df[target])
        recall = recall_score(df_test[target], predictions_df[target])
        f1 = f1_score(df_test[target], predictions_df[target])
        performance_dict.append({
            'Target': target,
            'Recall': recall,
            'F1-Score': f1,
            'Accuracy': accuracy
        })

    performance_df = pd.DataFrame(performance_dict)
    return performance_df

