import os
from sklearn.model_selection import train_test_split

# Global constant: Define the project root.
PROJECT_ROOT = os.getcwd()
visuals_path = os.path.join(PROJECT_ROOT, "predicting_customer_preference", "visuals")

# Import functions from your separate modules
from load_data import load_data
from data_preprocessing import preprocess_data, cap_outliers, log_transform
from EDA import plot_heatmaps, plot_categorical_features, plot_correlation_matrix, plot_product_counts, drop_unwanted_features
from model_training import train_and_evaluate_models, get_feature_importance, export_feature_importances_zipped
from final_model import predict_with_best_model
from model_evaluation import evaluate_model_on_test

def main():
    """
    Main function that executes the complete ML pipeline:
      1. Loads data from CSV files.
      2. Preprocesses data (merging, cleaning, transforming).
      3. Performs EDA on the full dataset and saves EDA plots.
      4. Drops irrelevant features ("balance" and "default").
      5. Splits the cleaned data into training and test sets.
      6. Trains and evaluates models via cross-validation.
      7. Saves the best models to a pickle file.
      8. Generates predictions on the held-out test set.
    """
    # ---------------------------
    # 1. Data Loading and preprocessing
    # ---------------------------
    customer_df, loans_df, customer_segments_df, products_df = load_data(PROJECT_ROOT)
    # Merge and preprocess the data into a single DataFrame.
    merged_df = preprocess_data(customer_df, loans_df, customer_segments_df, products_df)
    
    # ---------------------------
    # 2. Exploratory Data Analysis (EDA)
    # ---------------------------
    product_columns = ["has_investment_product", "has_credit_card", "has_fixed_deposit", "has_insurance"]
    categorical_features = ["job", "marital", "education", "default", "Segment"]
    numeric_features = ["income", "balance", "debt"]
    
    # Generate and save EDA plots.
    plot_heatmaps(merged_df, product_columns, visuals_path)
    plot_categorical_features(merged_df, categorical_features, visuals_path)
    plot_correlation_matrix(merged_df, numeric_features, visuals_path)
    plot_product_counts(products_df, visuals_path)
    
    # ---------------------------
    # 3. Feature Selection: Drop Irrelevant Features
    # ---------------------------
    # Based on EDA insights, drop only "balance" and "default".
    irrelevant_features = ["balance", "default"]
    cleaned_df = drop_unwanted_features(merged_df, irrelevant_features)

    # Apply outlier capping and log transformation to selected columns.
    cap_outliers(merged_df, 'debt')
    log_transform(merged_df, 'debt')
    
    # ---------------------------
    # 4. Train-Test Split
    # ---------------------------
    # Here we use 80% for training and 20% for testing.
    # Stratify using one target to ensure balanced splits.
    target_cols = ["has_investment_product", "has_credit_card", "has_fixed_deposit", "has_insurance"]
    df_train, df_test = train_test_split(
        cleaned_df,
        test_size=0.2,
        stratify=cleaned_df[target_cols[3]],
        random_state=42
    )
    
    # ---------------------------
    # 5. Model Training and Evaluation
    # ---------------------------
    # Define feature and target columns.
    feature_cols = ["income", "age", "job", "education", "dependents", "has_active_loan", "Segment", "marital"]
    
    # Define which features are categorical for the model.
    categorical_features_model = ["job", "education", "Segment", "marital"]
    numerical_features_model = list(set(feature_cols) - set(categorical_features_model))
    
    # Train and evaluate models on the training set using cross-validation.
    train_performance_df, best_models = train_and_evaluate_models(
        df=df_train,
        target_cols=target_cols,
        feature_cols=feature_cols,
        numerical_features=numerical_features_model,
        categorical_features=categorical_features_model
    )

    # Get 5 most influential features for predicting each product
    feature_importances = get_feature_importance(best_models)
    
    # Print performance metrics.
    print("Performance Metrics:")
    print(train_performance_df)
    print(feature_importances)
    export_feature_importances_zipped(feature_importances, PROJECT_ROOT, "predicting_customer_preference")
        
    # ---------------------------
    # 6. Model Prediction on Test Set
    # ---------------------------
    # Use the best models to generate predictions on the held-out test set.
    predictions_df = predict_with_best_model(df_test, feature_cols, best_models)
    predictions_df.to_csv(os.path.join(PROJECT_ROOT, "predicting_customer_preference", "product_recommendations.csv"), index=False)
    print("Predictions saved to product_recommendations.csv")

    test_performance_df = evaluate_model_on_test(predictions_df, df_test, target_cols)
    print(test_performance_df)

if __name__ == "__main__":
    main()
