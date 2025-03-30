import os
from measuring_campaign_roi.scripts.load_data import load_data
from measuring_campaign_roi.scripts.data_preprocessing import preprocess_data
from measuring_campaign_roi.scripts.eda import generate_eda_plots, generate_3d_roi_scatterplots
from measuring_campaign_roi.scripts.acquisition_cost_model import train_acquisition_cost_model
from measuring_campaign_roi.scripts.conversion_rate_model import train_conversion_rate_model
from measuring_campaign_roi.scripts.roi_model import train_roi_model
from measuring_campaign_roi.scripts.model_evaluation import evaluate_model_performance, evaluate_roi_model


def main():
    # ---- Paths ----
    project_root = os.getcwd()
    data_path = os.path.join(project_root, "data", "processed")
    visuals_path = os.path.join(project_root, "measuring_campaign_roi", "visuals")

    # ---- Load and preprocess data ----
    customer_df, campaigns_df, engagement_df = load_data()
    df = preprocess_data(customer_df, campaigns_df, engagement_df)

    # ---- Exploratory Data Analysis ----
    generate_eda_plots(df, visuals_path)

    # ---- Acquisition Cost Model ----
    X_cost = df[['campaign_type', 'campaign_duration', 'campaign_language']]
    y_cost = df['log_acquisition_cost']
    cat_cost = ['campaign_type', 'campaign_language']
    num_cost = ['campaign_duration']

    cost_model, preds_cost, true_cost, cost_coef_df = train_acquisition_cost_model(X_cost, y_cost, cat_cost, num_cost)
    print("ACQUISITION COST MODEL COEFFICIENTS")
    print(cost_coef_df)

    cost_metrics = evaluate_model_performance(preds_cost, true_cost, num_features=len(cost_coef_df))
    print("ACQUISITION COST MODEL EVALUATION")
    print(cost_metrics)

    # ---- Conversion Rate Model ----
    X_conv = df[['campaign_type', 'target_audience']]
    y_conv = df['conversion_rate']
    cat_conv = ['campaign_type', 'target_audience']

    conv_model, preds_conv, true_conv, conv_coef_df = train_conversion_rate_model(X_conv, y_conv, cat_conv)
    print("CONVERSION RATE MODEL COEFFICIENTS")
    print(conv_coef_df)

    conv_metrics = evaluate_model_performance(preds_conv, true_conv, num_features=len(conv_coef_df))
    print("CONVERSION RATE MODEL EVALUATION")
    print(conv_metrics)

    # ---- ROI Model ----
    roi_model, X_roi_scaled, scaler = train_roi_model(preds_conv, preds_cost, df['roi'])
    print("ROI MODEL COEFFICIENTS")
    print(dict(zip(['Conversion Rate', 'Cost'], roi_model.coef_)))

    mean_r2, mean_mse, mean_rmse = evaluate_roi_model(preds_conv, preds_cost, df['roi'])
    print("ROI MODEL EVALUATION")
    print(f"Mean R²: {mean_r2:.4f}")
    print(f"Mean MSE: {mean_mse:.4f}")
    print(f"Mean RMSE: {mean_rmse:.4f}")

    # ---- ROI 3D Visualization ----
    generate_3d_roi_scatterplots(df, preds_conv, preds_cost, visuals_path)


if __name__ == '__main__':
    main()
