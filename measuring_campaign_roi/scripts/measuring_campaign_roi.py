import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import os

## READING IN DATA
project_root = os.getcwd()  # Assumes script runs from project root
# Define the path to the processed data folder
data_path = os.path.join(project_root, "data", "processed")
# Load the CSV files
customer_df = pd.read_csv(os.path.join(data_path, "customer.csv"))
campaigns_df = pd.read_csv(os.path.join(data_path, "campaigns.csv"))
engagement_details_df = pd.read_csv(os.path.join(data_path, "engagement_details.csv"))
# Make visuals folder
visuals_path = os.path.join(project_root, "measuring_campaign_roi", "visuals")
os.makedirs(visuals_path, exist_ok=True)

############### Data Preprocessing ###############
# Obtaining derived variables 
# Join engagement_details with customer.csv on customer_id, adding CLV column
engagement_details_with_clv = engagement_details_df.merge(
    customer_df[['customer_id', 'customer_lifetime_value']],
    on='customer_id',
    how='left'
)

# Compute the average CLV per campaign
avg_clv_per_campaign = engagement_details_with_clv.groupby('campaign_id', as_index=False)['customer_lifetime_value'].mean()
avg_clv_per_campaign.rename(columns={'customer_lifetime_value': 'avg_clv'}, inplace=True)

# Merge campaigns.csv with avg_clv_per_campaign on campaign_id
merged_campaigns = campaigns_df.merge(avg_clv_per_campaign, on='campaign_id', how='left')

# Select and rearrange the required columns
df = merged_campaigns[['campaign_id', 'campaign_type', 'target_audience', 'campaign_duration',
                       'campaign_language', 'conversion_rate', 'acquisition_cost', 'avg_clv', 'roi']]

############### Exploratory Data Analysis ###############
# Summary statistics and pairplot to explore relationships
summary_stats = df.describe(include='all')

# Log-transform the acquisition_cost column due to high variance
df.loc[:, 'log_acquisition_cost'] = np.log(df['acquisition_cost'])
# Encode an order for target_audience
df.loc[:, 'target_audience'] = pd.Categorical(
    df['target_audience'], 
    ordered=True
)

# Configure grid for categorical feature vs CLV, Cost, Conversion Rate
fig, axes = plt.subplots(3, 3, figsize=(18, 14))
categorical_vars = ['campaign_type', 'target_audience', 'campaign_language']
numerical_targets = ['avg_clv', 'log_acquisition_cost', 'conversion_rate']
titles = ['CLV', 'Acquisition Cost', 'Conversion Rate']

# Plot boxplots for categorical features
for i, cat in enumerate(categorical_vars):
    for j, num in enumerate(numerical_targets):
        sns.boxplot(data=df, x=cat, y=num, ax=axes[i, j])
        axes[i, j].set_title(f'{titles[j]} by {cat.replace("_", " ").title()}')
        axes[i, j].tick_params(axis='x', rotation=45)

plt.tight_layout()
plot_path = os.path.join(visuals_path, "EDA_boxplots_categorical_vs_targets.png")
plt.savefig(plot_path)

# Plot lineplots for campaign_duration vs each numerical target
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for j, num in enumerate(numerical_targets):
    sns.lineplot(data=df, x="campaign_duration", y=num, ax=axes[j])
    axes[j].set_title(f'{titles[j]} by Campaign Duration')
    axes[j].set_xlabel("Campaign Duration (Days)")
    axes[j].set_ylabel(titles[j])

plt.tight_layout()
plot_path = os.path.join(visuals_path, "EDA_lineplots_duration_vs_targets.png")
plt.savefig(plot_path)

############### Acquisition Cost Sub-Model ###############
def cost_model(X, y, categorical_features, numerical_features):
    """
    Trains a linear regression model to predict cost
    Assumes that the target variable y is in log scale (e.g., log(cost)), and returns predictions
    transformed back to the original scale

    Parameters:
    - X: pd.DataFrame, feature matrix containing both categorical and numerical columns
    - y: pd.Series or np.ndarray, target variable (log(cost))
    - categorical_features: list of str, names of categorical columns in X
    - numerical_features: list of str, names of numerical columns in X

    Returns:
    - linreg_model: trained sklearn Pipeline with preprocessing and regression
    - preds: np.ndarray, predicted cost values in original scale (after exp transform)
    - true_vals: np.ndarray, actual cost values in original scale (after exp transform)
    - coef_df: pd.DataFrame, table of model coefficients showing:
        - Feature names
        - Log-scale coefficients
        - Approximate % change in cost for a one-unit increase in each feature
    """
    # Define preprocessor
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features),
        ('num', 'passthrough', numerical_features)
    ])

    # Define pipeline
    linreg_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # 5-fold cross-validation due to small dataset size
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Fit model
    linreg_model.fit(X, y)

    # Predict (log scale → original scale)
    log_preds = cross_val_predict(linreg_model, X, y, cv=kf)
    preds = np.expm1(log_preds)
    true_vals = np.expm1(y)

    # Coefficient interpretation
    feature_names = linreg_model.named_steps['preprocessor'].get_feature_names_out()
    log_coefficients = linreg_model.named_steps['regressor'].coef_
    percent_impact = (np.exp(log_coefficients) - 1) * 100

    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Log Coefficient': log_coefficients,
        'Approx % Change in Cost': percent_impact
    }).sort_values(by='Approx % Change in Cost', ascending=False)

    return linreg_model, preds, true_vals, coef_df

# function to evaluate model performance
def evaluate_model_performance(preds, true_vals, num_features):
    """
    Evaluates regression model performance using common metrics: 
    MSE, RMSE, R², and Adjusted R².

    Parameters:
    - preds: array-like, predicted values from the model (e.g., predicted cost or ROI)
    - true_vals: array-like, actual values (must be same length as preds)
    - num_features: int, number of features used in the model (for Adjusted R² calculation)

    Returns:
    - dict: a dictionary containing the following metrics:
        - "MSE": Mean Squared Error
        - "RMSE": Root Mean Squared Error
        - "R2": R-squared
        - "Adjusted R2": Adjusted R-squared

    Prints the evaluation metrics with appropriate formatting.
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

# Run cost model on the selected features
X = df[['campaign_type', 'campaign_duration', 'campaign_language']]
y = df['log_acquisition_cost']
cat_feats = ['campaign_type', 'campaign_language']
num_feats = ['campaign_duration']

model, preds_cost, true_vals, coef_df = cost_model(X, y, cat_feats, num_feats)
print("CONVERSION RATE MODEL COEFFICIENTS")
coef_df
print("\n")

# Evaluate cost_model
metrics = evaluate_model_performance(preds_cost, true_vals, num_features=coef_df.shape[0])
print("CONVERSION RATE MODEL EVALUATION")
metrics
print("\n")

############### Conversion Rate Sub-Model ###############
def conversion_model(X, y, categorical_features):
    
    """
    Trains a linear regression model to predict conversion rates using only categorical features.
    One-hot encoding is applied to categorical variables. Cross-validated predictions are used
    to evaluate model performance, and the learned coefficients are returned for interpretation.

    Parameters:
    - X: pd.DataFrame, feature matrix containing categorical columns
    - y: pd.Series or np.ndarray, target variable (conversion rate)
    - categorical_features: list of str, names of categorical columns in X

    Returns:
    - model: trained sklearn Pipeline with preprocessing and regression
    - preds: np.ndarray, predicted conversion rates using 5-fold cross-validation
    - y: np.ndarray or pd.Series, actual conversion rates (same as input `y`)
    - coef_df: pd.DataFrame, table showing:
        - Feature names (from one-hot encoded categories)
        - Corresponding linear regression coefficients (sorted by absolute value)
    """

    # Preprocessor (one-hot encoding for categorical features)
    preprocessor = ColumnTransformer(transformers=[
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ])

    # Pipeline with linear regression
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', LinearRegression())
    ])

    # Cross-validation setup
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    # Fit and predict using cross_val_predict
    model.fit(X, y)
    preds = cross_val_predict(model, X, y, cv=kf)

    # Coefficient extraction
    feature_names = model.named_steps['preprocessor'].get_feature_names_out()
    coefficients = model.named_steps['regressor'].coef_
    coef_df = pd.DataFrame({
        'Feature': feature_names,
        'Coefficient': coefficients
    }).sort_values(by='Coefficient', key=abs, ascending=False)

    return model, preds, y, coef_df

# Run conversion rate model on the selected features
X_conv = df[['campaign_type', 'target_audience']]
y_conv = df['conversion_rate']
cat_features_conv = ['campaign_type', 'target_audience']

model_conv, preds_conv, true_conv, coef_df_conv = conversion_model(X_conv, y_conv, cat_features_conv)
print("ACQUISITION COST MODEL COEFFICIENTS")
coef_df_conv
print("\n")


# Evaluate conversion rate model
metrics_conv = evaluate_model_performance(preds_conv, true_conv, num_features=coef_df_conv.shape[0])
print("ACQUISITION COST MODEL EVALUATION")
metrics_conv
print("\n")

############### ROI Model ###############
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(18, 8))

# Actual conversion rate & acquisition cost vs ROI
ax1 = fig.add_subplot(121, projection='3d')
sc1 = ax1.scatter(df['conversion_rate'], df['acquisition_cost'], df['roi'],
                  c=df['roi'], cmap='viridis', alpha=0.8)
ax1.set_xlabel("Conversion Rate")
ax1.set_ylabel("Acquisition Cost")
ax1.set_zlabel("ROI")
ax1.set_title("Actual: Conversion Rate & Acquisition Cost vs ROI")
fig.colorbar(sc1, ax=ax1, shrink=0.5, aspect=10)

# Predicted conversion rate & acquisition cost vs ROI
ax2 = fig.add_subplot(122, projection='3d')
sc2 = ax2.scatter(preds_conv, preds_cost, df['roi'],
                  c=df['roi'], cmap='viridis', alpha=0.8)
ax2.set_xlabel("Predicted Conversion Rate")
ax2.set_ylabel("Predicted Acquisition Cost")
ax2.set_zlabel("ROI")
ax2.set_title("Predicted: Conversion Rate & Acquisition Cost vs ROI")
fig.colorbar(sc2, ax=ax2, shrink=0.5, aspect=10)

plt.tight_layout()
plot_path = os.path.join(visuals_path, "scatterplot_conversion_cost_vs_roi.png")
plt.savefig(plot_path)
plt.close()

def predict_roi(preds_conv, preds_cost, y_roi):
    """
    Train a Linear Regression model using standardized predicted conversion and cost values.

    Parameters:
    - preds_conv: predicted conversion rates
    - preds_cost: predicted costs
    - y_roi: actual ROI values

    Returns:
    - model: trained LinearRegression instance
    - X_roi_scaled: standardized input matrix used for prediction
    - scaler: fitted StandardScaler instance (for inverse transforms if needed)
    """
    X_roi = np.column_stack([preds_conv, preds_cost])
    
    # Standardize features
    scaler = StandardScaler()
    X_roi_scaled = scaler.fit_transform(X_roi)
    
    # Train model
    model = LinearRegression()
    model.fit(X_roi_scaled, y_roi)
    
    return model, X_roi_scaled, scaler

model, X_roi_scaled, scaler = predict_roi(preds_conv, preds_cost, df['roi'])

coefficients = model.coef_
feature_names = ['Conversion Rate', 'Cost']

for name, coef in zip(feature_names, coefficients):
    print(f"{name} coefficient: {coef:.4f}")

print("ROI MODEL COEFFICIENTS")
metrics_conv
print("Conversion rate:", coefficients[0])
print("Cost:", coefficients[1])
print("\n")

def evaluate_roi_model(preds_conv, preds_cost, y_roi):
    """
    Evaluates a Linear Regression model using 3-fold CV

    Parameters:
    - preds_conv: predicted conversion rates (ouput of conversion_model)
    - preds_cost: predicted costs (ouput of cost_model)
    - y_roi: actual ROI values

    Returns:
    - mean_r2_roi: mean R² score from 3-fold CV
    - mean_mse: mean MSE from 3-fold CV
    - mean_rmse: mean RMSE from 3-fold CV
    """
    X_roi = np.column_stack([preds_conv, preds_cost])
    model = LinearRegression()
    
    # R² scores
    cv_scores_r2 = cross_val_score(model, X_roi, y_roi, cv=3, scoring='r2')
    mean_r2_roi = np.mean(cv_scores_r2)

    # Predictions for MSE and RMSE
    preds = cross_val_predict(model, X_roi, y_roi, cv=3)
    mean_mse = mean_squared_error(y_roi, preds)
    mean_rmse = np.sqrt(mean_mse)

    return mean_r2_roi, mean_mse, mean_rmse

mean_r2_roi, mean_mse, mean_rmse = evaluate_roi_model(preds_conv, preds_cost, df['roi'])

print("ROI MODEL EVALUATION")
print(f"Mean R²: {mean_r2_roi:.4f}")
print(f"Mean MSE: {mean_mse:.4f}")
print(f"Mean RMSE: {mean_rmse:.4f}")
print("\n")