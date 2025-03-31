import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV, train_test_split
from sklearn.metrics import precision_recall_curve, precision_recall_fscore_support, accuracy_score
from xgboost import XGBClassifier

def train_and_evaluate_models(df, target_cols, feature_cols, numerical_features, categorical_features):
    """
    Train and evaluate models using cross-validation for multiple binary targets.

    This function performs hyperparameter tuning, training, and evaluation (calculating recall,
    F1-score, and accuracy) for each target. It returns performance metrics and the best model,
    preprocessor, and threshold for each target.

    Args:
        df (pd.DataFrame): The training DataFrame.
        target_cols (list): List of target column names (binary classification).
        feature_cols (list): List of feature column names.
        numerical_features (list): List of numerical feature column names.
        categorical_features (list): List of categorical feature column names.

    Returns:
        performance_df (pd.DataFrame): DataFrame with average recall, F1-score, and accuracy for each target.
        best_models (dict): Dictionary containing the best model, preprocessor, and threshold for each target.
    """
    # Define hyperparameter grid for XGBoost
    param_grid = {
        'n_estimators': [50, 100, 500],
        'learning_rate': [0.01, 0.005, 0.05],
        'max_depth': [4, 6, 8],
        'min_child_weight': [1, 2, 3],
        'subsample': [0.7, 0.8, 1.0],
        'colsample_bytree': [0.7, 0.8, 1.0],
        'gamma': [0.1, 0.2, 0.3],
    }

    # Preprocessing pipeline for numerical and categorical features
    preprocessor = ColumnTransformer(transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="mean")),
            ("scaler", StandardScaler())
        ]), numerical_features),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical_features)
    ])

    # Set up cross-validation strategy
    kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    performance_metrics_all_targets = []
    best_models = {}

    for target in target_cols:
        X = df[feature_cols]
        y = df[target]

        # Compute scale_pos_weight for imbalanced classes
        neg_samples = (y == 0).sum()
        pos_samples = (y == 1).sum()
        scale_pos_weight = (neg_samples / pos_samples) if pos_samples != 0 else 1

        # Fit the preprocessor and transform the features
        X_processed = preprocessor.fit_transform(X)

        recall_list = []
        f1_list = []
        accuracy_list = []
        best_thresholds = []

        # Perform cross-validation
        for train_idx, val_idx in kf.split(X_processed, y):
            X_train, X_val = X_processed[train_idx], X_processed[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            # Update hyperparameter grid with current scale_pos_weight
            target_param_grid = param_grid.copy()
            target_param_grid['scale_pos_weight'] = [scale_pos_weight]

            random_search = RandomizedSearchCV(
                estimator=XGBClassifier(random_state=42, eval_metric="logloss"),
                param_distributions=target_param_grid,
                n_iter=10,
                scoring='accuracy',
                cv=3,
                verbose=0,
                n_jobs=-1,
                random_state=42
            )
            random_search.fit(X_train, y_train)
            best_model = random_search.best_estimator_

            # Predict probabilities and determine optimal threshold based on F1-score
            y_pred_proba = best_model.predict_proba(X_val)[:, 1]
            precision_vals, recall_vals, thresholds = precision_recall_curve(y_val, y_pred_proba)
            f1_scores = (2 * precision_vals * recall_vals) / (precision_vals + recall_vals + 1e-6)
            best_threshold = thresholds[np.argmax(f1_scores)]
            y_pred = (y_pred_proba > best_threshold).astype(int)

            _, recall, f1, _ = precision_recall_fscore_support(y_val, y_pred, average='binary')
            accuracy = accuracy_score(y_val, y_pred)

            recall_list.append(recall)
            f1_list.append(f1)
            accuracy_list.append(accuracy)
            best_thresholds.append(best_threshold)

        performance_metrics_all_targets.append({
            "Target": target,
            "Average Recall": np.mean(recall_list),
            "Average F1-Score": np.mean(f1_list),
            "Average Accuracy": np.mean(accuracy_list)
        })

        best_models[target] = {
            "preprocessor": preprocessor,
            "model": best_model,
            "threshold": np.mean(best_thresholds)
        }

    performance_df = pd.DataFrame(performance_metrics_all_targets)
    return performance_df, best_models

def get_feature_importance(best_models, top_n=5, plot=False):
    """
    Extract the top N feature importances for each target from the best models.

    Args:
        best_models (dict): Dictionary containing the best model for each target.
        top_n (int, optional): Number of top features to extract. Defaults to 5.
        plot (bool, optional): Whether to generate a plot of feature importances. Defaults to False.

    Returns:
        dict: A dictionary where each key is a target and each value is a DataFrame of feature importances.
    """
    feature_importance_dict = {}
    for target, components in best_models.items():
        model = components["model"]
        preprocessor = components["preprocessor"]

        # Retrieve one-hot encoded feature names if available
        try:
            ohe = preprocessor.named_transformers_['cat'].named_steps['encoder']
            cat_features = preprocessor.transformers_[1][2]
            ohe_feature_names = list(ohe.get_feature_names_out(cat_features))
        except Exception:
            ohe_feature_names = []

        num_features = preprocessor.transformers_[0][2]
        all_features = list(num_features) + ohe_feature_names

        importance = model.feature_importances_
        importance_df = pd.DataFrame({
            "Feature": all_features,
            "Importance": importance
        }).sort_values(by="Importance", ascending=False).head(top_n)

        feature_importance_dict[target] = importance_df

        if plot:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(8, 5))
            plt.barh(importance_df["Feature"][::-1], importance_df["Importance"][::-1])
            plt.xlabel("Importance")
            plt.title(f"Top {top_n} Feature Importances for Target: {target}")
            plt.tight_layout()
            plt.show()

    return feature_importance_dict
