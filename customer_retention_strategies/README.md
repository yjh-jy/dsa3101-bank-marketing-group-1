# Customer Retention Strategies

How can we predict and mitigate customer churn using machine learning?

This module implements a machine learning pipeline to assess customer churn risk and support retention strategies. It leverages Random Forest models to generate churn risk scores using key behavioral and financial indicators.

## Overview

Customer churn remains a critical challenge for banks, especially when involving high-value customers. In this project, we developed a machine learning model that enables early detection of at-risk customers by analyzing their digital activity, financial behavior, and product engagement.

## Objectives

- Build a churn prediction model using Random Forest Classifier.
- Identify top indicators of churn such as digital inactivity, low product engagement, and high debt-to-income ratio.
- Generate actionable churn risk scores and categories for CRM integration.
- Recommend automated interventions to reduce churn.

## Key Insights

- **Digital Inactivity** and **low engagement with products** are top predictors of customer churn.
- Customers with **high debt-to-income ratios** are significantly more likely to churn.
- The model enables real-time churn scoring for each customer, enabling preemptive action.
- Integrating churn predictions with CRM systems allows for **automated retention workflows**, personalized offers, and intervention by relationship managers.

## Expected Outcome

1. **Churn Prediction Engine:**  
   A trained model that calculates churn probability scores.

2. **Risk Segmentation Report:**  
   CSV output (`churn_warning_report.csv`) that categorizes customers into Low, Medium, or High churn risk.

3. **Visualizations:**  
   Feature importance and class distribution plots to understand model behavior.

## Folder Structure
```
customer_retention/ 
├── scripts/ 
│ └── customer_retention_strategies.py # Main ML logic 
├── visuals/ # Plots and graphs 
├── churn_warning_report.csv # Final churn score for CRM integration
│── Dockerfile                      # Docker container setup
│── README.md                       # Module-specific documentation
│── requirements.txt                # Import required packages
└── run_scripts.sh                  # Bash script to coordinate all the script runs
│── customer_retention_strategies.md                       # Analysis report
```

## Methodology

1. **Data Merging & Feature Engineering:**  
   Customer data merged from multiple sources, then enriched with features like total products owned, digital usage frequency, and debt-to-income ratio.

2. **Churn Labeling:**  
   Customers inactive for over 6 months or with unpaid loans beyond 12 months were flagged as churn risks.

3. **Model Training:**  
   A Random Forest Classifier was trained using balanced datasets via SMOTE.

4. **Evaluation & Visualization:**  
   Performance metrics and feature importance plots were generated for interpretability.

5. **Reporting:**  
   Final churn scores and risk levels were saved in a CSV for CRM integration.

## Usage

Once the Docker environment is set up, you can run all analysis scripts with:
```
./run_scripts.sh
```

The plots will be saved in 'visuals/' and the CSV output file will be generated


## Strategic Impact

Integrating this model into the bank's CRM system enables:
- **Proactive Retention Campaigns** via personalized communication
- **Efficient Use of Relationship Managers' Time** by focusing on high-risk individuals
- **Revenue Protection** by intervening before churn materializes

This ML-powered approach provides a scalable and seamless method for customer retention with minimal change to existing workflows.

---
