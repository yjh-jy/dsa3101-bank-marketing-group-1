# Predicting Customer Preference

This repository contains scripts and visualizations for predicting customer product preferences. It includes supporting functions for data preprocessing, exploratory data analysis (EDA), visualization, model training, evaluation, and final prediction of customer preferences.

## Project Structure

```
predicting_customer_preference/
├── scripts/
│   ├── data_preprocessing.py     # Data cleaning and preprocessing
│   ├── EDA.py                    # Exploratory data analysis and visualization
│   ├── final_model.py            # Final model to predict customer preferences
│   ├── load_data.py              # Data loading script
│   ├── main.py                   # Main execution pipeline
│   └── model_evaluation.py       # Model performance evaluation
│   ├── model_training.py         # Model training and evaluation
├── visuals/                      # Auto-generated plots (EDA output)
│   ├── categorical_features.png
│   ├── correlation_matrix.png
│   ├── heatmaps_active_loans.png
│   └── product_counts.png
├── README.md                     # Project overview and usage
├── requirements.txt              # Project dependencies
└── customer_preferences.md       # Detailed documentation
```

## Key Features

### Data Preprocessing
**`scripts/data_preprocessing.py`**

- Cleans and preprocesses data to aggregate customer behaviour, format featyres, and perform feature scaling.

### Exploratory Data Analysis (EDA)
**`scripts/EDA.py`**

- Provides exploratory analysis with visualizations to uncover key insights and identify patterns for model and feature selection.

### Model Training
**`scripts/model_training.py`**

- Performs hyperparameter tuning on our model and cross-validates their initial performance.

### Final Model Prediction
**`scripts/final_model.py`**

- Deploys the final optimized model to predict customer preferences based on trained insights.

### Model Evaluation
**`scripts/model_evaluation.py`**

- Assesses predictive model accuracy using metrics such as accuracy, F1 score, and recall.


## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:
```
./run_scripts.sh
```
All generated plots will be automatically saved in the `visuals/` folder.

## Documentation and Standards

Detailed project documentation can be found in [`customer_preferences.md`](customer_preferences.md).
