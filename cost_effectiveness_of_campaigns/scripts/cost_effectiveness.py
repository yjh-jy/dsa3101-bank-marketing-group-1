import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, cross_val_predict, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


# Load the necessary datasets
campaigns = pd.read_csv('../../data/processed/campaigns.csv')
customers = pd.read_csv('../../data/processed/customer.csv')
engagements = pd.read_csv('../../data/processed/engagement_details.csv')

# Merge the datasets
merged_df = pd.merge(campaigns, engagements, on='campaign_id', how='left')

def calculate_personalisation_score(merged_df):
    """
    Calculates the personalisation score for each campaign.

    Returns
    - pandas.DataFrame, original DataFrame with an additional column 'personalisation_score'.
    """
    # Define campaign type weights
    campaign_type_weights = {
        'Search Engine Optimisation': 0.2,
        'Email Marketing': 0.8,
        'Affiliate Marketing': 0.5,
        'Display Advertising': 0.3
    }

    def get_personalisation_score(row):
        # Language score based on campaign language
        language_score = 0.5 if row['campaign_language'] in ['Mandarin', 'French', 'Spanish', 'German'] else 0.3

        # Target audience score based on age group
        if row['target_audience'] == '35-44':
            target_audience_score = 0.7
        elif row['target_audience'] == '55+':
            target_audience_score = 0.6
        else:
            target_audience_score = 0.5

        # Duration score based on campaign duration
        if row['campaign_duration'] > 60:
            duration_score = 0.8
        elif row['campaign_duration'] > 30:
            duration_score = 0.6
        else:
            duration_score = 0.4

        # Campaign type score based on predefined weights
        campaign_type_score = campaign_type_weights.get(row['campaign_type'], 0.4)

        # Calculate the final personalisation score
        personalisation_score = (
            0.25 * campaign_type_score +
            0.2 * language_score + 
            0.25 * target_audience_score +
            0.3 * duration_score
        )

        return personalisation_score

    merged_df['personalisation_score'] = merged_df.apply(get_personalisation_score, axis=1)

    return merged_df

def calculate_engagement_score(merged_df):
    """
    Calculates the engagement score for each campaign.

    Returns:
    - pandas.DataFrame, original DataFrame with an additional column 'engagement_score'.
    """
    # Aggregate engagement data by campaign_id
    campaign_engagements = merged_df.groupby('campaign_id').agg(
        total_engagements=('has_engaged', 'sum'),
        total_duration=('duration', 'sum'),
        impressions=('impressions', 'first')
    ).reset_index()

    # Calculate the engagement rate and effective engagement rate
    campaign_engagements['engagement_rate'] = campaign_engagements['total_engagements'] / campaign_engagements['impressions']
    campaign_engagements['effective_engagement_rate'] = campaign_engagements['total_duration'] / campaign_engagements['impressions']

    # Calculate the final engagement score
    campaign_engagements['engagement_score'] = (
        0.5 * campaign_engagements['engagement_rate'] + 
        0.5 * campaign_engagements['effective_engagement_rate']
    )

    merged_df = pd.merge(merged_df, campaign_engagements[['campaign_id', 'engagement_score']], on='campaign_id', how='left')

    return merged_df

# Calculate the personalisation score and engagement score for each campaign.
merged_df = calculate_personalisation_score(merged_df)
merged_df = calculate_engagement_score(merged_df)

def preprocess_data(df):
    """
    Preprocesses the data for modelling by encoding categorical features and defining 
    features and target variable.

    Returns:
    - X: pandas.DataFrame, the feature set for modelling.
    - y: pandas.Series, the target variable for modelling.
    - label_encoder: sklearn.preprocessing.LabelEncoder, the fitted LabelEncoder 
    used to transform the categorical variables.
    """
    # Encode categorical features using LabelEncoder
    label_encoder = LabelEncoder()
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    
    for col in categorical_features:
        df[col] = label_encoder.fit_transform(df[col])
    
    # Define features (X) and target variable (y)
    X = df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]
    y = df['personalisation_score']
    
    return X, y, label_encoder


def train_personalisation_model(df):
    """
    Trains a Random Forest model to predict the personalisation score for a campaign.

    Returns:
    - personalisation_model: sklearn.ensemble.RandomForestRegressor, the trained Random Forest
    model for predicting the personalisation score.
    - label_encoder: sklearn.preprocessing.LabelEncoder, the fitted LabelEncoder 
    used to transform the categorical variables.
    """
    # Preprocess the data
    X, y, label_encoder = preprocess_data(df)
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train the Random Forest Regressor
    personalisation_model = RandomForestRegressor(n_estimators=100, random_state=42)
    personalisation_model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = personalisation_model.predict(X_test)
    
    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared (R²): {r2}")
    
    return personalisation_model, label_encoder

def predict_personalisation_score(new_campaign_df, personalisation_model, label_encoder):
    """
    Predicts the personalisation score for a new campaign using a trained model.

    Returns:
    - float: The predicted personalisation score for the new campaign.
    """
    # List of categorical features
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    
    # Encode categorical features only (skip numerical columns like 'campaign_duration')
    for col in categorical_features:
        new_campaign_df[col] = label_encoder.fit_transform(new_campaign_df[col])

    # Define the features to be used in the model 
    X_new = new_campaign_df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]

    # Predict the personalization score using the trained model
    predicted_personalisation_score = personalisation_model.predict(X_new)
    
    return predicted_personalisation_score[0]

# Train and obtain the personalisation model
personalisation_model, label_encoder = train_personalisation_model(merged_df)

# Define new campaign data to test the model
new_campaign_data = {
    'campaign_type': 'Email Marketing',  # Example new label
    'campaign_language': 'Mandarin',
    'target_audience': '35-44',
    'campaign_duration': 45
}
new_campaign_df = pd.DataFrame([new_campaign_data])

# Predict the personalisation score for the new campaign
predicted_personalisation_score = predict_personalisation_score(new_campaign_df, personalisation_model, label_encoder)
print(f"Predicted Personalization Score: {predicted_personalisation_score}")

def preprocess_data(df):
    """
    Preprocesses the data for modelling by encoding categorical features and 
    defining features and target variable.

    Returns:
    X: pandas.DataFrame, the features set for modelling.
    y: pandas.Series, the target variable for modelling.
    label_encoder: sklearn.preprocessing.LabelEncoder, the fitted LabelEncoder 
    used to transform the categorical variables.
    """
    # Instantiate the LabelEncoder
    label_encoder = LabelEncoder()

    # Encode categorical features: campaign_type, campaign_language, target_audience
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    for col in categorical_features:
        df[col] = label_encoder.fit_transform(df[col])
    
    # Define features (X) and target variable (y)
    X = df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]
    y = df['engagement_score'] 
    
    return X, y, label_encoder

def train_engagement_model(df):
    """
    Trains a Random Forest model to predict the engagement score for a campaign.

    Returns:
    - engagement_model: sklearn.ensemble.RandomForestRegressor, the trained Random Forest
    model for predicting the engagement score.
    - label_encoder: sklearn.preprocessing.LabelEncoder, the fitted LabelEncoder 
    used to transform the categorical variables.
    """
    # Preprocess the data (encode categorical features)
    X, y, label_encoder = preprocess_data(df)
    
    # Split data into training and testing sets (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the RandomForestRegressor model
    engagement_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model using the training data
    engagement_model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = engagement_model.predict(X_test)
    
    # Evaluate the model's performance
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared (R²): {r2}")
    
    return engagement_model, label_encoder

# Function to predict the engagement score for new campaign data
def predict_engagement_score(new_campaign_df, engagement_model, label_encoder):
    """
    Predicts the engagement score for a new campaign using a trained model.

    Returns:
    - float: The predicted engagement score for the new campaign.
    """
    # Encode the categorical features in the new data
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    
    for col in categorical_features:
        new_campaign_df[col] = label_encoder.fit_transform(new_campaign_df[col])

    # Define the features to be used in the model
    X_new = new_campaign_df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]

    # Predict the engagement score using the trained model
    predicted_engagement_score = engagement_model.predict(X_new)
    
    return predicted_engagement_score[0]

# Train and obtain the engagement model
engagement_model, label_encoder = train_engagement_model(merged_df)

# Predict the engagement score for the new campaign
predicted_engagement_score = predict_engagement_score(new_campaign_df, engagement_model, label_encoder)
print(f"Predicted Engagement Score: {predicted_engagement_score}")

def preprocess_data(df):
    """
    Preprocesses the data for modelling by encoding categorical features and defining 
    features and target variable.

    Returns:
    - X: pandas.DataFrame, the feature set for modelling.
    - y: pandas.Series, the target variable for modelling.
    - label_encoder: sklearn.preprocessing.LabelEncoder, the fitted LabelEncoder 
    used to transform the categorical variables.
    """
    label_encoder = LabelEncoder()
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    
    # Apply LabelEncoder to each categorical feature
    for col in categorical_features:
        df[col] = label_encoder.fit_transform(df[col])
    
    # Define features (X) and target variable (y)
    X = df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]
    y = df['acquisition_cost']
    
    return X, y, label_encoder

def train_cost_model(df):
    """
    Trains a Random Forest model to predict te acquisition cost.

    Returns:
    - cost_model: sklearn.ensemble.RandomForestRegressor: The trained Random Forest model
    for predicting the acquisition cost.
    - label_encoder: sklearn.preprocessing.LabelEncoder: The fitted LabelEncodeer used to 
    transform categorical variables during preprocessing.
    - scaler: sklearn.preprocessing.MinMaxScaler: The fitted MinMaxScaler used to scale
    the target variable.
    """
    X, y, label_encoder = preprocess_data(df)
    
    # Initialize MinMaxScaler
    scaler = MinMaxScaler()
    
    # Scale the acquisition cost (y) to the range [0, 1]
    y_scaled = scaler.fit_transform(y.values.reshape(-1, 1))
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y_scaled, test_size=0.2, random_state=42)
    
    # Initialize the RandomForestRegressor model
    cost_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    # Train the model using the training data
    cost_model.fit(X_train, y_train)
    
    # Make predictions on the test set
    y_pred = cost_model.predict(X_test)
    
    # Evaluate the model's performance
    mae = mean_absolute_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred, squared=False)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Cost Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae}")
    print(f"Root Mean Squared Error (RMSE): {rmse}")
    print(f"R-squared (R²): {r2}")
    
    return cost_model, label_encoder, scaler

def predict_acquisition_cost(new_campaign_df, cost_model, label_encoder, scaler):
    """
    Predicts the acquisition cost for a new campaign using a trained model.

    Returns:
    - float: The predicted acquisition cost for the new campaign.
    """
    # Encode the categorical features in the new data
    categorical_features = ['campaign_type', 'campaign_language', 'target_audience']
    
    for col in categorical_features:
        new_campaign_df[col] = label_encoder.transform(new_campaign_df[col])

    # Define the features to be used in the model
    X_new = new_campaign_df[['campaign_type', 'campaign_language', 'target_audience', 'campaign_duration']]

    # Predict the acquisition cost using the trained model
    predicted_acquisition_cost = cost_model.predict(X_new)
    
    # Reverse the scaling to get the acquisition cost on the original scale
    predicted_acquisition_cost = scaler.inverse_transform(predicted_acquisition_cost.reshape(-1, 1))
    
    # Return the first prediction
    return predicted_acquisition_cost[0][0]

# Train the cost model and obtain the trained model.
cost_model, cost_label_encoder, cost_scaler = train_cost_model(merged_df)

# Predict the acquisition cost for the new campaign.
predicted_acquisition_cost = predict_acquisition_cost(new_campaign_df, cost_model, cost_label_encoder, cost_scaler)
print(f"Predicted Acquisition Cost: {predicted_acquisition_cost}")

def calculate_cost_benefit_ratio(new_campaign_df, personalisation_model, engagement_model, cost_model, label_encoder, cost_scaler):
    """
    Calculates the cost-benefit ratio for a new campaign using predicted personalisation
    scores, engagement scores and acquisition costs.

    Returns:
    - normalised_acquisition_cost: float, the normliased acquisition cost for the new campaign.
    - personalisation_score: float, the predicted personalisation score for the new campaign.
    - engagement_score: float, the predicted engagement score for the new campaign.
    - cost_benefit_ratio: float, the calculated cost-benefit ratio.
    """
    # Predict the personalisation score using the personalisation model
    personalisation_score = predict_personalisation_score(new_campaign_df, personalisation_model, label_encoder)
    
    # Predict the engagement score using the engagement model
    engagement_score = predict_engagement_score(new_campaign_df, engagement_model, label_encoder)
    
    # Predict the acquisition cost using the cost model
    predicted_acquisition_cost = predict_acquisition_cost(new_campaign_df, cost_model, label_encoder, cost_scaler)
    
    # Normalize the acquisition cost to be between 0 and 1
    normalized_acquisition_cost = cost_scaler.transform([[predicted_acquisition_cost]])[0][0]  # Reshape and scale
    
    # Calculate the benefit (weighted sum of personalisation and engagement scores)
    benefit = 0.5 * personalisation_score + 0.5 * engagement_score  # You can adjust the weights based on your criteria
    
    # Calculate the Cost-Benefit Ratio
    cost_benefit_ratio = normalized_acquisition_cost / benefit
    cost_benefit_ratio = min(cost_benefit_ratio, 1)
    
    return normalized_acquisition_cost, personalisation_score, engagement_score, cost_benefit_ratio

# Calculate the cost-benefit ratio for the new campaign
normalized_acquisition_cost, personalisation_score, engagement_score, cost_benefit_ratio = calculate_cost_benefit_ratio(
    new_campaign_df, personalisation_model, engagement_model, cost_model, cost_label_encoder, cost_scaler
)

# Print the results
print(f"Acquisition Cost: {predicted_acquisition_cost}")
print(f"Personalisation Score: {personalisation_score}")
print(f"Engagement Score: {engagement_score}")
print(f"Cost-Benefit Ratio: {cost_benefit_ratio}")

def calculate_cost_benefit_for_df(merged_df, personalisation_model, engagement_model, cost_model, label_encoder, cost_scaler):
    """
    Calculates the cost-benefit ratio for each campaign in the dataset

    Returns: 
    - pandas.DataFrame
    """
    result_data = []
    
    # Loop through each campaign and calculate the cost-benefit ratio
    for _, row in merged_df.iterrows():
        campaign_df = pd.DataFrame([row])  # Get a single campaign as a DataFrame
        
        # Calculate the cost-benefit ratio for this campaign
        normalized_acquisition_cost, personalisation_score, engagement_score, cost_benefit_ratio = calculate_cost_benefit_ratio(
            campaign_df, personalisation_model, engagement_model, cost_model, label_encoder, cost_scaler
        )
        
        # Store the results in the list
        result_data.append({
            'campaign_type': row['campaign_type'],
            'target_audience': row['target_audience'],
            'cost_benefit_ratio': cost_benefit_ratio
        })
    
    # Convert the result data into a DataFrame
    result_df = pd.DataFrame(result_data)
    return result_df

# Calculate the cost-benefit ratios for the entire dataset
result_df = calculate_cost_benefit_for_df(merged_df, personalisation_model, engagement_model, cost_model, cost_label_encoder, cost_scaler)

# Aggregate duplicates by taking the mean of the cost-benefit ratio for each combination
result_df = result_df.groupby(['target_audience', 'campaign_type'], as_index=False)['cost_benefit_ratio'].mean()

# Pivot the result_df to create a matrix suitable for a heatmap
heatmap_data = result_df.pivot(index='target_audience', columns='campaign_type', values='cost_benefit_ratio')

# Drop any rows and columns that contain NaN values
heatmap_data = heatmap_data.dropna(axis=0, how='all')  # Drop rows with all NaN values
heatmap_data = heatmap_data.dropna(axis=1, how='all')  # Drop columns with all NaN values

# Create a heatmap to visualize the cost-benefit ratio
plt.figure(figsize=(12, 6))

# Create the heatmap with annotations
sns.heatmap(heatmap_data, annot=True, cmap='coolwarm', fmt='.2f', cbar_kws={'label': 'Cost-Benefit Ratio'}, 
            xticklabels=heatmap_data.columns, yticklabels=heatmap_data.index)

# Set plot title
plt.title('Cost-Benefit Ratio Heatmap by Campaign Type and Target Audience')

# Set axis labels
plt.xlabel('Campaign Type')
plt.ylabel('Target Audience')

# Show the plot
# plt.show()