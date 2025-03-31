import numpy as np
import pandas as pd
import os
import zipfile
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
    preprocessor, threshold, and averaged feature importances for each target.
    """
    from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder
    from sklearn.metrics import precision_recall_curve, precision_recall_fscore_support, accuracy_score
    from xgboost import XGBClassifier
    import numpy as np
    import pandas as pd

    param_grid = {
        'n_estimators': [50, 100, 500],
        'learning_rate': [0.01, 0.005, 0.05],
        'max_depth': [4, 6, 8],
        'min_child_weight': [1, 2, 3],
        'subsample': [0.7, 0.8, 1.0],
        'colsample_bytree': [0.7, 0.8, 1.0],
        'gamma': [0.1, 0.2, 0.3],
    }

    kf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    performance_metrics_all_targets = []
    best_models = {}

    for target in target_cols:
        X = df[feature_cols]
        y = df[target]

        neg_samples = (y == 0).sum()
        pos_samples = (y == 1).sum()
        scale_pos_weight = (neg_samples / pos_samples) if pos_samples != 0 else 1

        recall_list = []
        f1_list = []
        accuracy_list = []
        best_thresholds = []
        fold_importances = []
        final_preprocessor = None

        for train_idx, val_idx in kf.split(X, y):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

            preprocessor = ColumnTransformer(transformers=[
                ("num", Pipeline([
                    ("imputer", SimpleImputer(strategy="mean")),
                    ("scaler", StandardScaler())
                ]), numerical_features),
                ("cat", Pipeline([
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
                ]), categorical_features)
            ])

            X_train_proc = preprocessor.fit_transform(X_train)
            X_val_proc = preprocessor.transform(X_val)

            final_preprocessor = preprocessor

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
            random_search.fit(X_train_proc, y_train)
            best_model = random_search.best_estimator_

            try:
                ohe = preprocessor.named_transformers_['cat'].named_steps['encoder']
                cat_features = preprocessor.transformers_[1][2]
                ohe_feature_names = list(ohe.get_feature_names_out(cat_features))
            except Exception:
                ohe_feature_names = []

            num_features = preprocessor.transformers_[0][2]
            all_features = list(num_features) + ohe_feature_names

            importances = pd.Series(best_model.feature_importances_, index=all_features)
            fold_importances.append(importances)

            y_pred_proba = best_model.predict_proba(X_val_proc)[:, 1]
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

        avg_importances = pd.concat(fold_importances, axis=1).mean(axis=1).sort_values(ascending=False).reset_index()
        avg_importances.columns = ["Feature", "Importance"]

        performance_metrics_all_targets.append({
            "Target": target,
            "Average Recall": np.mean(recall_list),
            "Average F1-Score": np.mean(f1_list),
            "Average Accuracy": np.mean(accuracy_list)
        })

        best_models[target] = {
            "preprocessor": final_preprocessor,
            "model": best_model,
            "threshold": np.mean(best_thresholds),
            "feature_importances": avg_importances
        }

    performance_df = pd.DataFrame(performance_metrics_all_targets)
    return performance_df, best_models

def get_feature_importance(best_models, top_n=5, plot=False):
    import matplotlib.pyplot as plt

    feature_importance_dict = {}
    for target, components in best_models.items():
        importance_df = components["feature_importances"].head(top_n)
        feature_importance_dict[target] = importance_df

        if plot:
            plt.figure(figsize=(8, 5))
            plt.barh(importance_df["Feature"][::-1], importance_df["Importance"][::-1])
            plt.xlabel("Importance")
            plt.title(f"Top {top_n} Feature Importances for Target: {target}")
            plt.tight_layout()
            plt.show()

    return feature_importance_dict


def export_feature_importances_zipped(feature_importances_dict, project_root, folder, output_zip_name='feature_importances.zip'):
    """
    Exports each target's feature importances DataFrame as a CSV file, zips them together,
    and outputs the zip file in the specified folder under the project root.

    Args:
        feature_importances_dict (dict): Dictionary where each key is a target and each value is a 
                                         DataFrame of feature importances.
        project_root (str): The root directory of the project.
        folder (str): The subfolder under the project root where the output will be stored.
        output_zip_name (str): Name of the output zip file.
    """
    # Construct the full output directory.
    output_dir = os.path.join(project_root, folder)
    os.makedirs(output_dir, exist_ok=True)
    
    csv_files = []
    
    # Save each DataFrame as a CSV file in the output directory.
    for target, importance_df in feature_importances_dict.items():
        csv_filename = os.path.join(output_dir, f"feature_importances_{target}.csv")
        importance_df.to_csv(csv_filename, index=False)
        csv_files.append(csv_filename)
    
    # Define the full path for the zip file.
    output_zip_path = os.path.join(output_dir, output_zip_name)
    
    # Create a zip archive and add each CSV file.
    with zipfile.ZipFile(output_zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for csv_filename in csv_files:
            # Store only the file name in the zip.
            zipf.write(csv_filename, arcname=os.path.basename(csv_filename))
    
    # Remove the individual CSV files after zipping.
    for csv_filename in csv_files:
        os.remove(csv_filename)
    
    print(f"Exported feature importances to feature_importances.zip")
