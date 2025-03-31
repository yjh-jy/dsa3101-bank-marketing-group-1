# Behavioural Patterns

## Overview

This module aims to analyze behavioural patterns across different customer segments. By examining product usage, transaction history, and digital engagement, the analysis identifies key behavioural patterns that inform targeted marketing strategies. The insights will help tailor approaches to specific customer segments, increasing the effectiveness of marketing efforts.

---

## Folder Structure

```
behvioural_patterns/
├── insights/
│   └── visualizations/             # Folder containing output visualizations
│   └── behavioural_patterns.md     # Markdown file containing key insights and targeted marketing approaches
├── scripts/
|   └── analysis_functions.py       # Functions for performing various analyses and visualizations
│   └── behavioural_patterns.py     # Main analysis     
│   └── utils.py                    # Utility functions for data loading and transformation
│── README.md                       # Project overview and instructions
└── requirements.txt                # Import required packages
```

---

## File Descriptions

| Path | Description |
|------|-------------|
| `behavioural_patterns/insights/visualizations/` | Directory where all generated charts and plots are saved after running the script. |
| `behavioural_patterns/insights/behavioural_patterns.md` | Markdown file containing key insights from the analysis, including targeted marketing approaches for each customer segment. It also includes visualizations. |
| `behavioural_patterns/scripts/analysis_functions.py` | Contains functions that perform the analysis and generate visualizations (e.g., NPS analysis, financial health, product usage, transactions, and digital engagement). |
| `behavioural_patterns/scripts/behavioural_patterns.py` | Main Analysis Script: This file serves as the entry point for the module. It orchestrates the data loading, preparation, and analysis workflow by calling functions from utils.py and analysis_functions.py. The script imports utility functions for tasks such as data loading, preparation, and transformation (including loan categorization and transaction classification), and then executes various analysis functions to generate insights and visualizations. Note that visualizations are generated programmatically and closed automatically (using `plt.close()`), unless modified to display interactively. |
| `behavioural_patterns/scripts/utils.py` | Contains utility functions for data loading, preparation, and helper methods such as `categorize_loan_purpose` and `classify_money_flow`. |
| `behavioural_patterns/README.md` | Documentation file for the behavioural patterns module, including an overview of the project, details of the analysis methodology, and setup instructions. |
| `behavioural_patterns/requirements.txt` | Lists all the Python packages and their versions required to run the analysis. This ensures a consistent development environment across different systems. |

---

## Prerequisite

Ensure that the following environment is set up:
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

---

## How To Run
This module is dockerised and should be run from the project root directory due to file path dependencies.

### 1. Ensure Docker containers are running
From project root:
```bash
docker ps | grep behavioural_patterns
```

### 2. Run the pipeline
From project root:
```bash
./behavioural_patterns/run_scripts.sh
```

---

## Script Execution Order
For this module, only one script needs to be executed:
```bash
behavioural_patterns/scripts/behavioural_patterns.py
```

---

## Dependencies
All required Python packages for this module are listed in:
```bash
behavioural_patterns/requirements.txt
```
If package versions used do not match those in requirements.txt, a package mismatch warning will appear in terminal.
Follow the printed instructions to fix

---

## Expected Outcome

- **Detailed Insights:**  
  A comprehensive analysis that highlights differences in behavioural patterns among various segments.

- **Actionable Strategies:**  
  Specific recommendations for targeted marketing based on the identified patterns.

- **Data Visualization:**  
  Charts and graphs that visually represent the differences in customer behaviour across segments.

## Description of Datasets Used

- **customers:** Contains demographic, financial, and account information for each customer.

- **loans:** Details of loans taken by customers, including loan amounts, purposes, and repayment dates.

- **products:** Information about the products each customer holds, such as investment products, credit cards, personal loans, fixed deposits, and insurance.

- **transactions:** Transactional data, capturing transaction type, amount, and date for each customer.

- **digital_usage:** Tracks customers' usage of digital platforms, including mobile app and web account activity, login frequency, and time spent on these platforms.

## Methodology

1. **Data Preparation:**  
   Merge data from internal sources and perform data cleaning and transformation.

2. **Segmentation:**  
   Use the customer_segments.csv file, generated from the customer_segmentation folder, for customer segmentation analysis.

3. **Exploratory Data Analysis (EDA):**  
   Apply statistical tests, such as the chi-square test, and visualization techniques, including bar plots, heatmaps, and boxplots, to identify data patterns across customer segments.

4. **Pattern Identification:**  
   Analyze key behaviors, including on-time loan payments, product usage trends, transactional habits, and digital engagement levels, to uncover significant patterns within the data.

5. **Recommendation Development:**  
   Translate the insights into targeted marketing recommendations for each customer segment.

---