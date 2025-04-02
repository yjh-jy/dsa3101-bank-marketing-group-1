# Data Directory Overview

This directory contains organized datasets and related resources for the DSA3101 Bank Marketing Project. Below is a breakdown of its structure and contents.

## Directory Structure

- `processed/` - The main dataset used for this project, which is partially synthetic.
- `raw/` - Original, unprocessed datasets sourced from Kaggle.
- `scripts/` - Python scripts used to generate synthetic data.
- `visuals/` - Visualizations generated during script runs, used to verify various statistical properties.
- `Data_Schema.csv` - A CSV file detailing the schema of the datasets.
- `Dockerfile` - Docker container setup
- `README.md` - Module-specific documentation
- `requirements.txt ` - Python dependencies
- `run_scripts.sh `  - Bash script to coordinate all the script runs

## Contents

### `processed/`
The processed directory contains the primary dataset used for this project. It consists of mostly synthetic data, ensuring privacy while maintaining statistical integrity and business relevance.

### `raw/`
This directory holds the original, unaltered datasets that serve as the source data for the project. All datasets are sourced from Kaggle.

### `scripts/`
The Python scripts in this folder are responsible for generating the synthetic data used in the `processed` directory. These scripts apply transformations to raw data while preserving essential statistical properties and incorporating key business assumptions outlined in `Data_Schema`. Most scripts incorporate randomization, meaning that datasets generated in separate runs are NOT guaranteed to be identical or fully reproducible. Our current analysis and models are trained using the existing ones found in `processed`.

### `visuals/`
This folder contains visualizations created during the execution of the scripts. These visualizations are used to validate statistical properties and ensure the quality of the synthetic data. 

### `Data_Schema.csv`
A schema file providing details on the structure of the datasets, including field names, data types, and descriptions.

## Usage Notes (IMPORTANT)

- The `processed` directory contains the main datasets used in the project. Any modifications should be documented and versioned appropriately.
- The `scripts` directory contains code for generating synthetic data. Any changes to these scripts should be reviewed to ensure they preserve statistical properties.
- Randomization is applied to most scripts when generating synthetic data, so datasets produced in different runs are not guaranteed to be fully reproducible. **DO NOT rerun the scripts unless you have git tracking enabled or else you risk permenantly altering the current tables in `processed`, which may cause our analysis and models to be inconsistent.**
- Visualizations stored in `visuals` serve as verification tools for synthetic data quality.

## How To Run
This module is dockerised and should be run from the project root directory due to file path dependencies.

### 1. Ensure Docker container is running
From project root:
```bash
docker ps | grep data
```

### 2. Run the data generation pipeline
From project root:
```bash
./data/run_scripts.sh
```

For more details about the project, refer to the main [README.md](https://github.com/yjh-jy/dsa3101-bank-marketing-group-1/blob/main/README.md) in the repository.
