# Cost Effectiveness of Campaigns

## Overview

This module analyses how to balance personalisation with cost-effectiveness in marketing campaigns based on campaign, engagement and customer data.

---

## Project Structure

```
cost_effectiveness_of_campaigns/
├── markdown/                         
│   ├── cost_effectiveness.md         # Detailed documentation
├── scripts/
│   ├── cost_effectiveness.py         # Cost-benefit analysis
├── visuals/                          # Auto-generated plots
│   ├── cost_benefit_ratio_heatmap.png
│   ├── personalisation_potential_heatmap.png
│   ├── personalisation_potential_scores.png
│── Dockerfile                      # Docker container setup
│── README.md                       # Module-specific documentation
│── requirements.txt                # Import required packages
└── run_scripts.sh                  # Bash script to coordinate all the script runs
```

---

## Datasets Used

- **campaigns**: Contains information about various marketing campaigns, such as campaign type, language, target audience etc.
- **engagement_details**: Details regarding customer engagement with various capaigns, such as duration and impression.
- **customer**: Contains demographic and behavioural information about the customers.

---

## Key Features

- **Feature Engineering**: Calcuation of personalisation score, calculation of the engagement score, preprocessing data functions that handle encoding categorical features and defining the features and target variables, and calculating customer personalisation potential.
- **Predictive Models**: Trained and utilised several models, including a personalisation model, engagement model, cost model and cost-benefit ratio calculation.
- **Model Evaluation**: Assesses the predictive models according to relevant metrics.

---

## How to Run

Once the Docker environment is set up, you can run all analysis scripts with:
```bash
./run_scripts.sh
```

---

## Documentation and Standards

All script dependencies will be managed automatically via Docker.
