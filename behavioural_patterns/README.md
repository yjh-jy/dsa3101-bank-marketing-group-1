# Behavioural Patterns

## Overview

This module aims to analyze behavioural patterns across different customer segments. By examining product usage, transaction history, and digital engagement, the analysis identifies key behavioural patterns that inform targeted marketing strategies. The insights will help tailor approaches to specific customer segments, increasing the effectiveness of marketing efforts.

---

## Objectives

- **Segment Analysis:**  
  Examine how customer behaviours vary across different segments.

- **Behavioural Insights:**  
  Analyze patterns in product usage, transaction history, and digital engagement.

- **Targeted Recommendations:**  
  Use the insights gained to recommend tailored marketing approaches for each customer segment.

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

##  How to Run the Python Script

1. **Clone the repository**
```bash
git clone <repository-url>
```

2. **Check current working directory**
```bash
pwd
# should end in dsa3101-bank-marketing-group-1
```

3. **Dependencies: Install required Python packages**
```bash
pip install -r requirements.txt
```

4. **Run the Python scripts in the specified order**

The scripts should be executed in the following order:

- First, run `utils.py`: This script contains utility functions for loading and preparing data. It must be executed first to ensure the necessary data is available for analysis.

```bash
# Run this in terminal
python behavioural_patterns/scripts/utils.py
```
```bash
# If above code does not work in macbook terminal:
python3 behavioural_patterns/scripts/utils.py
```

- Next, run `analysis_functions.py`: This script includes various functions for analyzing customer behaviour, financial health, product usage, and more. It should be run after utils.py to utilize the prepared data.

```bash
# Run this in terminal
python behavioural_patterns/scripts/analysis_functions.py
```
```bash
# If above code does not work in macbook terminal:
python3 behavioural_patterns/scripts/analysis_functions.py
```

- Finally, run `behavioural_patterns.py`: This script is the main execution file that integrates the functions from `utils.py` and `analysis_functions.py`. It should be run last to perform the full analysis and generate the insights.

```bash
# Run this in terminal
python behavioural_patterns/scripts/behavioural_patterns.py
```
```bash
# If above code does not work in macbook terminal:
python3 behavioural_patterns/scripts/behavioural_patterns.py
```

---

## Generating Visualizations

To generate and display visualizations from the analysis script, follow these steps:

1. Add the following lines after each chunk of the visualization code in behavioural_patterns.py to display the visualizations interactively:
```bash
plt.tight_layout()
plt.show()
```

2. Comment out or remove plt.close() to allow the visualizations to pop up interactively. This will ensure that the generated plots are displayed during script execution.