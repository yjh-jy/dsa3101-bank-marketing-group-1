# Customer & Campaign Engagement Analysis

This repository contains scripts and supporting functions for customer-level and campaign-level engagement analysis, including feature engineering, exploratory data analysis (EDA), data quality checks, and business rule flagging.

---

## Project Structure

```plaintext
customer_engagement/
├── scripts/
│   ├── customer_engagement.py        # Customer-level analysis
│   ├── campaign_engagement.py        # Campaign-level analysis
│   ├── utils.py                      # Common data quality, loading, and EDA functions
│   ├── feature_engineering.py        # Feature engineering logic
│   └── business_rules.py             # Business rule flagging functions
├── figures/                          # Auto-generated plots (EDA output)
│── Dockerfile                        # Docker container setup
│── engagement_summary.md             # Business interpretation and key findings
│── README.md                         # Module-specific documentation
│── requirements.txt                  # Import required packages
└── run_scripts.sh                    # Bash script to coordinate all the script runs
```

---

## Key Features

- **Customer-level engagement analysis**  
  `scripts/customer_engagement.py`  
  Merges and processes customer, transaction, and digital usage data to derive insights on high-value users and their engagement behavior.

- **Campaign-level engagement analysis**  
  `scripts/campaign_engagement.py`  
  Analyzes campaign performance metrics including engagement rate, CTR, and campaign attributes.

- **Utility functions**  
  `scripts/utils.py`  
  Provides reusable functions for:
  - Data quality checks
  - Missing value imputation
  - Data loading
  - EDA plotting

- **Feature engineering**  
  `scripts/feature_engineering.py`  
  Contains logic for creating engagement flags, summarizing transactions, and engineering digital usage metrics.

- **Business rule functions**  
  `scripts/business_rules.py`  
  Defines customer segmentation criteria (e.g., high-value, multichannel, recent activity).

---

## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:

```bash
./run_scripts.sh
```

All output plots will be saved automatically in the `figures/` folder.

---

## Documentation and Standards

All script dependencies will be managed automatically via Docker.