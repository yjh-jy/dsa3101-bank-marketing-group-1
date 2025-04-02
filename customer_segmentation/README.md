# Customer Segmentation

This module performs customer segmentation based on transaction data and customers' behaviours/attributes.

---

## Prerequisites

Ensure the following dependencies are installed before running the system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

---

## Project Structure

```
customer_segmentation/
├── scripts/
│   ├── utils.py                       # Contains functions with segmentation logic
│   ├── segmentation.py                # Contains main functions
├── markdown/
│   └── segmentation.md                # For project documentation and to summarize insights
├── visuals/                           # Output boxplots auto-saved here
│   └── boxplots_for_outliers.png
│   └── post_winsorize_boxplots_for_outliers.png
│── customer_segments.csv              # Input data file
│── Dockerfile                         # Docker container setup
│── README.md                          # Module-specific documentation
│── requirements.txt                   # Import required packages
└── run_scripts.sh                     # Bash script to coordinate all the script runs
```

---

## File Descriptions

| Path | Description |
|------|-------------|
| `customer_segmentation/scripts/segmentation.py` | **Main execution script.** Calls the functions from `utils.py` to perform customer segmentation, handle missing values, outlier treatment, clustering, and labeling. Also generates boxplots and outputs a processed CSV file with customer segments (`customer_segments_rerun.csv`). |
| `customer_segmentation/scripts/utils.py` | **Contains all reusable functions** for data loading, preprocessing, handling missing values, feature engineering, outlier detection and treatment, scaling, clustering, labeling, and saving outputs. This file organizes the segmentation logic into modular functions. |
| `customer_segmentation/customer_segments.csv` | **Reference output data file** containing customer id with their segmentation. This is the version used for analysis and exploration. The output CSV file generated after running `segmentation.py` will be named `customer_segments_rerun.csv`, but analysis will refer to `customer_segments.csv` to ensure consistency across different environments. |
| `customer_segmentation/markdown/segmentation.md` | **Project documentation** and business logic explanation. Summarizes the methodology used in `segmentation.py`, key data characteristics, assumptions, and insights derived from customer segmentation. Meant for clean and structured explanation. |
| `customer_segmentation/visuals/` | **Folder to store visual outputs** such as boxplots generated during the segmentation process. Example files include `boxplots_for_outliers.png` and `post_winsorize_boxplots_for_outliers.png` to compare data distributions before and after outlier treatment. |
| `customer_segmentation/README.md` | **Project-level documentation.** Provides an overview of the customer segmentation module, instructions to run the scripts, dependencies, and folder structure. Meant for onboarding or for others to quickly understand how to use the module. |
| `customer_segmentation/requirements.txt` | Lists all the Python packages and their versions required to run the segmentation pipeline. This ensures a consistent development environment across different systems. |

---

## How To Run
This module is dockerised and should be run from the project root directory due to file path dependencies.

### 1. Ensure Docker containers are running
From project root:
```bash
docker ps | grep customer_segmentation
```

### 2. Run the segmentation pipeline
From project root:
```bash
./customer_segmentation/run_scripts.sh
```

---

## Script Execution Order
For this module, only one script needs to be executed:
```bash
customer_segmentation/scripts/segmentation.py
```

---

## Dependencies
All required Python packages for this module are listed in:
```bash
customer_segmentation/requirements.txt
```
If package versions used do not match those in requirements.txt, a package mismatch warning will appear in terminal.
Follow the printed instructions to fix

---

## How to Check If It Ran Correctly

1. Boxplots named **`boxplots_for_outliers.png`** and **`post_winsorize_boxplots_for_outliers.png`** should appear in:
   ```
   /customer_segmentation/visuals
   ```

2. The terminal should print:
   ```
   Saved 'customer_segments.csv' with Customer ID & segment name
   ```

3. A file named `customer_segments_rerun.csv` should be saved under:
   ```
   /customer_segmentation/
   ```

---

## Output Summary

### 1. `customer_segments_rerun.csv`

This CSV file contains:
- `Customer_ID`: The unique customer identifier
- `Segment`: Assigned segment label for each customer

Segmentation is done using the **KMeans algorithm**, based on customer behavioural features such as balance and transaction frequency.
The random_state parameter produces deterministic results on a specific OS, but does not produce the same results on different OSes. Hence, any further analysis will be ran on the `customer_segments.csv` instead of the `customer_segments_rerun.csv` obtained from further reruns. 

Segment labels and meanings:

| Segment | Behaviour |
|---------|-----------|
| **High-value** | Frequent transactions, high balance, high income, engaged in digital banking |
| **Budget-conscious** | Lower balance, lower transaction frequency, avoids unnecessary fees and services |
| **At risk / inactive customers** | Minimal or no recent transactions, high churn risk |

---

### 2. Boxplots (under `/visuals`)

- `boxplots_for_outliers.png`: Shows raw feature distributions before outlier treatment
- `post_winsorize_boxplots_for_outliers.png`: Shows distributions after applying winsorization

These visuals help explain the variation in customer behavior across segments.

---

### 3. Package mismatch output

When running the segmentation script, if packages used are not the same packages required, a message and a reminder to install the correct packages will be printed. The script will still run but please download the necessary packages and run again.

---
