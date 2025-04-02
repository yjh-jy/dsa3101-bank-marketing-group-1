# Predicting Customer Preferences

This repository contains scripts and visualizations for predicting customer product preferences. It includes supporting functions for data preprocessing, exploratory data analysis (EDA), visualization, model training, evaluation, and final prediction of customer preferences.

## Project Structure

```
predicting_customer_preference/
├── results/
│   ├── feature_importances.csv         # Top features influencing product predictions
│   └── product_recommendations.csv     # Final product recommendations for each customer
├── scripts/
│   ├── data_preprocessing.py           # Data cleaning and preprocessing
│   ├── EDA.py                          # Exploratory data analysis and visualization
│   ├── final_model.py                  # Final model to predict customer preferences
│   ├── load_data.py                    # Data loading script
│   ├── main.py                         # Main execution pipeline
│   ├── model_evaluation.py             # Model performance evaluation
│   └── model_training.py               # Model training and evaluation
├── visuals/                            # Auto-generated plots (EDA output)
│   ├── categorical_features.png
│   ├── correlation_matrix.png
│   ├── heatmaps_active_loans.png
│   └── product_counts.png
│── Dockerfile                          # Docker container setup
│── predicting_customer_preferences.md  # Detailed documentation
│── README.md                           # Module-specific documentation
│── requirements.txt                    # Import required packages
└── run_scripts.sh                      # Bash script to coordinate all the script runs
```

## Key Features

### Data Preprocessing
**`scripts/data_preprocessing.py`**

- Cleans and preprocesses raw data to consolidate customer loan behavior, format feature inputs, and perform scaling for modeling.

### Exploratory Data Analysis (EDA)
**`scripts/EDA.py`**

- Performs exploratory analysis with visualizations to uncover key insights and identify patterns for model and feature selection.

### Model Training
**`scripts/model_training.py`**

- Conducts hyperparameter tuning and cross-validation to evaluate initial model performance and identify optimal modeling parameters.

### Final Model Prediction
**`scripts/final_model.py`**

- Implements the optimized predictive model to forecast customer preferences.

### Model Evaluation
**`scripts/model_evaluation.py`**

- Evaluates model accuracy and predictive capability using performance metrics such as accuracy, precision, recall, and F1 score.

### Results Output
**`results/`**

- Contains reference output files generated from the final model run. These are the versions used for all analysis, visualizations, and reporting in this submission.
- `product_recommendations.csv` provides customer IDs along with their predicted product preferences.
- `feature_importances.csv` lists the top features influencing predictions for each target product.
- The output CSV files generated after running `main.py` will be named `product_recommendations_rerun.csv` and `feature_importances_rerun.csv` in the same folder to preserve the original analysis version.

## Key Visualisations

Key visual outputs from exploratory data analysis are stored in the `visuals/` directory:

- **Heatmaps of Active Loans vs Product Ownership:** [`heatmaps_active_loans.png`](visuals/heatmaps_active_loans.png)  
  *Visualizes the relationship between customer product ownership and active loan status using heatmaps.*

- **Categorical Feature Distributions:** [`categorical_features.png`](visuals/categorical_features.png)  
  *Bar plots showing distributions of key categorical variables to uncover trends and potential feature importance.*

- **Correlation Matrix:** [`correlation_matrix.png`](visuals/correlation_matrix.png)  
  *Heatmap displaying correlations among numerical features, aiding in feature selection.*

- **Product Ownership Counts and Rates:** [`product_counts.png`](visuals/product_counts.png)  
  *Bar charts illustrating the number of customers owning each product and the relative ownership rates.*

## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:
```
./run_scripts.sh
```
All generated plots will be automatically saved in the `visuals/` folder. The rerun output predictions of the model on the test set will be saved in the results folder.

## Documentation and Standards

All script dependencies will be managed automatically via Docker.