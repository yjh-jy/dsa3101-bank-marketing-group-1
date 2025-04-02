# Personalised Campaigns in Bank Marketing

## Project Overview

This project, developed as part of the DSA3101 AY24/25 Semester 2 curriculum, focuses on analyzing bank marketing strategies to enhance customer engagement and optimize campaign effectiveness. The primary objective is to leverage data analytics and machine learning to design personalized marketing campaigns that helpthe bank by segmenting customers based on behaviors and preferences, predicting future customer needs, and optimizing marketing campaigns in real time to boost engagement and ROI.

## Repository Structure

The repository is organized as follows (this is a rough structure, and each module may contain additional files such as data, notebooks, or documentation):

```
├── behavioural_patterns/             # Analyzes customer behaviors to identify trends
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── campaign_impact_analysis/         # Assesses the effectiveness of past marketing campaigns
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── campaign_optimization/            # Optimizes marketing campaigns for efficiency
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── cost_effectiveness_of_campaigns/  # Evaluates financial efficiency of campaigns
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── customer_engagement/              # Investigates methods to enhance customer interaction
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── customer_retention_strategies/    # Develops approaches to maintain customer relationships
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── customer_segmentation/            # Segments customer base for tailored marketing
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── data/                             # Contains datasets for analyses
├── measuring_campaign_roi/           # Calculates ROI for different marketing campaigns
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── predicting_customer_preference/   # Forecasts customer preferences using analytics
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── segmentation_updates/             # Updates and refines customer segmentation methodologies in real-time
│   └── run_scripts.sh                # Bash script to run module-specific scripts
├── .gitignore                        # .gitignore file to ignore metadata
├── docker-compose.yaml               # Docker compose config file for orchestrating the modules
├── give_permissions.sh               # Optional bash script, run only if permissions is insufficient
├── README.md                         # Overall README documentation
```

## Getting Started

### Prerequisites

Ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/standalone/) (if running on Linux)
- [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yjh-jy/dsa3101-bank-marketing-group-1.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd dsa3101-bank-marketing-group-1
   ```

3. **Build and start the containers**:

   ```bash
   docker-compose up -d --build
   ```

   This will build and start the containers, but it **will not automatically execute any scripts.**

4. **Manually run the scripts in Bash terminal**: After the containers are up and running, navigate to each module directory and execute the respective bash script:

   ```bash
   cd <module_directory>
   ./run_scripts.sh
   ```

   Optionally, you can also run from the root:

   ```bash
   ./<module_directory>/run_scripts.sh
   ```

DISCLAIMER: Do not use a virtual environment or your global environment to run this project, because the file paths are prioritized to be compatible with Docker container environments thus running some scripts with your own environments might produce unexpected results. In general, using `python` or `python3` to run the scripts is NOT guranteed to work.

### Troubleshooting

1. Encountered `Permission denied` when running `./run_scripts.sh`:

Run the following to give permissions recursively to all `.sh` scripts in this project:
   ```bash
   chmod +x give_permissions.sh
   ./give_permissions.sh   
   ```

## Usage

Each sub-directory contains specific analyses related to bank marketing strategies. To utilize the analyses:

1. Navigate to the relevant directory.
2. Open the Jupyter Notebook files (`.ipynb`), Python scripts (`.py`), or Markdown files (`.md`) to explore the analyses and insights.
3. Follow any instructions provided within the notebooks, scripts, or markdown files to replicate the analyses or input new data.

## Contributing

Contributions to this project are welcome. If you have suggestions for improvements or new analyses, please fork the repository and submit a pull request. Ensure that your contributions align with the project's objectives and maintain code quality standards.

