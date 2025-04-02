# Campaign Impact Analysis

This module evaluates the effectiveness of marketing campaigns by analyzing customer responses and identifying key factors that influence campaign success.

## Objectives

- Develop a framework for measuring the success of marketing campaigns using key performance indicators (KPIs) such as engagement rate, conversion rate, and customer lifetime value (CLV).

## Expected Outcome

1. **Actionable Insights:**  
   Propose specific strategies to improve marketing campaigns based on the analysis of KPIs.

2. **Enhanced Measurement Framework:**  
   A robust framework for assessing campaign success using data-driven metrics.

3. **Visualizations:**  
   Charts and graphs that illustrate key findings, saved in the `visuals/` folder.

## Project Structure

```
campaign_impact_analysis/
├── notebooks/                      # Notebooks used during analysis, to be deleted
├── scripts/
│   └── campaign_impact_analysis.py # Main analysis logic
├── insights/
│   ├── visuals/                    # Folder containing output visualizations
│   └── campaign_impact_analysis.md # Key insights of the module
├── requirements.txt                # Python dependencies
└── README.md                       # Document for campaign impact analysis module
```

## Methodology

1. **Data Loading and Preparation:**  
   Load processed campaign, customer, and engagement data from the `data/processed/` folder. Merge datasets to create a comprehensive view of campaign performance. Perform feature engineering, such as calculating age-target alignment and engagement metrics.

2. **Exploratory Data Analysis (EDA):**  
   Analyze campaign reach, engagement rates, and conversion rates. Use visualizations to identify trends, such as engagement by channel, monthly performance, and customer segment distribution.

3. **KPI Analysis:**  
   Evaluate key performance indicators (KPIs) such as reach, engagement rate, conversion rate, and customer lifetime value (CLV). Identify correlations between engagement and conversion rates, and assess the effectiveness of targeting high-value customers.

4. **Insights and Recommendations:**  
   Derive actionable insights, such as optimizing campaign scheduling, improving alignment with target audiences, and focusing on specific customer segments. Propose strategies to enhance marketing effectiveness based on data-driven findings.

## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:
```
./run_scripts.sh
```
All generated plots will be automatically saved in the `insights/visuals/` folder.

## Documentation and Standards

All script dependencies will be managed automatically via Docker.
