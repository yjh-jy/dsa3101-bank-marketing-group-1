import os
from sklearn.model_selection import train_test_split
from load_data import load_data
from data_preprocessing import preprocess_data
from eda import plot_boxplots, plot_lineplots, plot_3d_roi
from acquisition_cost_model import train_acquisition_cost_model
from conversion_rate_model import train_conversion_rate_model
from roi_model import train_roi_model, predict_roi_model
from model_evaluation import evaluate_model_performance


def main():
    # ---- Paths ----
    project_root = os.getcwd()
    data_path = os.path.join(project_root, "data", "processed")
    visuals_path = os.path.join(project_root, "visuals")

    # ---- Load and preprocess data ----
    customer_df, campaigns_df, engagement_df = load_data(data_path)
    df = preprocess_data(customer_df, campaigns_df, engagement_df)

    # ---- Exploratory Data Analysis ----
    plot_boxplots(df, visuals_path)
    plot_lineplots(df, visuals_path)

    # ---- Split data into training and testing ----
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=1)

    # ---- Acquisition Cost Model ----
    X_cost_train = train_df[['campaign_type', 'campaign_duration', 'campaign_language']]
    y_cost_train = train_df['log_acquisition_cost']
    cat_cost = ['campaign_type', 'campaign_language']
    num_cost = ['campaign_duration']

    cost_model, preds_cost_train, true_cost, cost_coef_df = train_acquisition_cost_model(X_cost_train, y_cost_train, cat_cost, num_cost)
    print("ACQUISITION COST MODEL COEFFICIENTS")
    print(cost_coef_df)
    print("\n")

    # Predictions on test set
    X_cost_test = test_df[['campaign_type', 'campaign_duration', 'campaign_language']]
    preds_cost_test = cost_model.predict(X_cost_test)
    true_cost_test = test_df['log_acquisition_cost']

    cost_metrics = evaluate_model_performance(preds_cost_test, true_cost_test, num_features=len(cost_coef_df))
    print("ACQUISITION COST MODEL EVALUATION")
    print(cost_metrics)
    print("\n")

     # ---- Conversion Rate Model ----
    X_conv_train = train_df[['campaign_type', 'target_audience']]
    y_conv_train = train_df['conversion_rate']
    cat_conv = ['campaign_type', 'target_audience']

    conv_model, preds_conv_train, _, conv_coef_df = train_conversion_rate_model(X_conv_train, y_conv_train, cat_conv)
    print("CONVERSION RATE MODEL COEFFICIENTS")
    print(conv_coef_df)
    print("\n")

    # Predictions on test set
    X_conv_test = test_df[['campaign_type', 'target_audience']]
    preds_conv_test = conv_model.predict(X_conv_test)
    true_conv_test = test_df['conversion_rate']

    conv_metrics = evaluate_model_performance(preds_conv_test, true_conv_test, num_features=len(conv_coef_df))
    print("CONVERSION RATE MODEL EVALUATION")
    print(conv_metrics)
    print("\n")

    # ---- ROI Model ----
    roi_model, __, roi_scaler = train_roi_model(preds_conv_train, preds_cost_train, train_df['roi'])
    print("ROI MODEL COEFFICIENTS")
    print(dict(zip(['Conversion Rate', 'Cost'], roi_model.coef_)))
    print("\n")

    preds_roi_test = predict_roi_model(roi_model, roi_scaler, preds_conv_test, preds_cost_test)

    roi_metrics = evaluate_model_performance(preds_roi_test, test_df['roi'], num_features=2)
    print("ROI MODEL TEST EVALUATION")
    print(roi_metrics)
    print("\n")

    # ---- Save predictions to CSV ----
    predictions_df = test_df.copy()
    predictions_df['predicted_roi'] = preds_roi_test
    predictions_df.to_csv(os.path.join(project_root, "output", "output_predictions.csv"), index=False)

    # ---- ROI 3D Visualization ----
    plot_3d_roi(test_df, preds_conv_test, preds_cost_test, visuals_path)

if __name__ == '__main__':
    main()