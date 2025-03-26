# Behavioural Patterns

## Overview

This module aims to analyze customer behaviours across different segments. By examining product usage, transaction history, and digital engagement, the analysis identifies key behavioural patterns that inform targeted marketing strategies. The insights will help tailor approaches to specific customer segments, increasing the effectiveness of marketing efforts.

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
│   └── behavioural_patterns.py     # Main analysis logic     
└── README.md                       # Project overview and instructions
```

---

## File Descriptions

| Path | Description |
|------|-------------|
| `behavioural_patterns/insights/visualizations/` | Directory where all generated charts and plots are saved after running the script. |
| `behavioural_patterns/insights/behavioural_patterns.md` | Markdown file containing key insights from the analysis, including targeted marketing approaches for each customer segment. It also includes visualizations. |
| `behavioural_patterns/scripts/behavioural_patterns.py` | Python script containing the core analysis logic, including data preprocessing, identification of key behavioral patterns, and the creation of visualizations. Visualizations are generated but do not appear as popups, as they are closed automatically using plt.close(). |
| `behavioural_patterns/README.md` | Documentation file for the behavioural patterns module, including an overview of the project, details of the analysis methodology, and setup instructions. |

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
pip install pandas==2.2.3 numpy==1.23.1 seaborn==0.13.2 matplotlib==3.10.1 scipy==1.9.0 
```

4. **Run the Python script**
```bash
# Run this in terminal
python behavioural_patterns/scripts/behavioural_patterns.py
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