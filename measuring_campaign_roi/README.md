# Measuring Campaign ROI

This repository contains scripts and visualizations for predicting and analyzing the Return on Investment (ROI) of marketing campaigns. It includes data loading, preprocessing, exploratory data analysis (EDA), modeling, and evaluation scripts, along with insightful visualizations.

---

## Project Structure

```plaintext
measuring_campaign_roi/
├── output/
│   └── output_predictions.csv        # Predicted ROI from ROI model
├── scripts/
│   ├── acquisition_cost_model.py     # Acquisition cost predictive model
│   ├── conversion_rate_model.py      # Conversion rate predictive model
│   ├── data_preprocessing.py         # Data cleaning and preprocessing
│   ├── eda.py                        # Exploratory data analysis and visualization
│   ├── load_data.py                  # Data loading script
│   ├── main.py                       # Main execution pipeline
│   ├── model_evaluation.py           # Model performance evaluation
│   └── roi_model.py                  # ROI predictive modeling
├── visuals/                          # Auto-generated plots (EDA output)
│   ├── 3d_roi_scatterplots.png
│   ├── boxplots_categorical_vs_targets.png
│   └── lineplots_duration_vs_targets.png
│── Dockerfile                      # Docker container setup
│── README.md                       # Module-specific documentation
│── requirements.txt                # Import required packages
└── run_scripts.sh                  # Bash script to coordinate all the script runs
```

---

## Key Features

- **Data Loading and Preprocessing**  
  `scripts/load_data.py`, `scripts/data_preprocessing.py`  
  Loads raw data and performs essential data cleaning, formatting, and feature preparation.

- **Exploratory Data Analysis (EDA)**  
  `scripts/eda.py`  
  Generates exploratory visualizations and statistical summaries to uncover key insights and patterns for model and feature selection

- **Predictive Models**  
  `scripts/acquisition_cost_model.py`, `scripts/conversion_rate_model.py`, `scripts/roi_model.py`  
  Trains and builds predictive models for key metrics; acquisition cost, conversion rate, and ROI

- **Model Evaluation**  
  `scripts/model_evaluation.py`  
  Assesses predictive model accuracy and performance using appropriate metrics.

## Key Visualisations

Key visual outputs are stored in the `visuals/` directory:
- **ROI Scatterplot**: 3d_roi_scatterplots.png
- **Analysis of categorical campaign features vs. CLV, cost and conversion rate**: boxplots_categorical_vs_targets.png
- **Analysis of campaign duration vs CLV, cost and conversion rate**: lineplots_duration_vs_targets.png
---

## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:

```bash
./run_scripts.sh
```

All output plots will be saved automatically in the `visuals/` folder.
The output predictions of the ROI model on the test set will be saved in `output_predictions.csv`.

---

## Documentation and Standards

All script dependencies will be managed automatically via Docker.
