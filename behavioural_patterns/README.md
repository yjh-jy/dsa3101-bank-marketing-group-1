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

- **customers**
  Contains demographic, financial, and account information for each customer.

- **loans:**  
  Details of loans taken by customers, including loan amounts, purposes, and repayment dates.

- **products:**  
  Information about the products each customer holds, such as investment products, credit cards, personal loans, fixed deposits, and insurance.

- **transactions:**  
  Transactional data, capturing transaction type, amount, and date for each customer.

- **digital_usage**
  Tracks customers' usage of digital platforms, including mobile app and web account activity, login frequency, and time spent on these platforms.

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
├── notebooks/
│   └── behvioural_patterns.ipynb   # Main analysis notebook
├── scripts/
│   └── behavioural_patterns.py     # Main analysis logic     
├── visualizations/                 # Folder for saving output visualizations
└── README.md                       # Project overview and instructions
```

---

## File Descriptions

| Path | Description |
|------|-------------|
| `behavioural_patterns/notebooks/behavioural_patterns.ipynb` | Notebook containing the main analysis, including exploratory data analysis (EDA), data visualizations, key insights from the analysis, and targeted marketing approaches for each customer segment. |
| `behavioural_patterns/notescripts/behavioural_patterns.py` | Python script containing the core analysis logic, including data preprocessing and key behavioral pattern identification. Does not include data visualizations, insights, or targeted marketing strategies. |
| `behavioural_patterns/visualizations/` | Directory where all generated charts and plots are saved after running the analysis notebook or script. |
| `behavioural_patterns/README.md` | Documentation file for the behavioural patterns module, including an overview of the project, setup instructions, and details of the analysis methodology. |

---

## Prerequisite

Ensure that the following environment is set up:
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

---

##  How to Run the python notebook and script

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
pip install pandas==2.2.3 numpy==1.23.1 seaborn==0.13.2 matplotlib==3.10.1 scipy==1.9.0 jupyter
```

4. **Run the Python notebook**
```bash
- If Jupyter is installed and recognized:
# Run this in terminal
python behavioural_patterns/notebooks/behavioural_patterns.ipynb

- If not recognized, try:
python -m notebook behavioural_patterns/notebooks/behavioural_patterns.ipynb
```
5. **Run the Python script**
```bash
# Run this in terminal
python behavioural_patterns/scripts/behavioural_patterns.py
```
---