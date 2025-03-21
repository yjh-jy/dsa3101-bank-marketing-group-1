# Customer Segmentation

This module performs customer segmentation based on transaction data and customers' behaviours/attributes.

---

## Folder Structure

```
customer_segmentation/
├── scripts/
│   ├── segmentation.py                # Main segmentation logic
│   └── customer_segments.csv          # Input data file
├── notebook/
│   └── segmentation.ipynb             # For visual EDA and exploratory segmentation
├── visuals/                           # Output boxplots auto-saved here
└── README.md
```

---

## File Descriptions

| Path | Description |
|------|-------------|
| `customer_segmentation/scripts/segmentation.py` | Main script that performs customer segmentation using input features (e.g., balance, transaction amount). Also generates boxplots and outputs a CSV file. |
| `customer_segmentation/scripts/customer_segments.csv` | Input data file containing customer features for segmentation. |
| `customer_segmentation/notebook/segmentation.ipynb` | Includes business logic and explanation of code in segmentation.py. Jupyter Notebook version for cleaner, visual exploration of segmentation logic and data characteristics (for presentation / EDA). |
| `customer_segmentation/visuals/` | Folder where generated boxplots will be saved after running the script. |
| `customer_segmentation/README.md` | Documentation for the customer segmentation module. |

---

##  How to Run

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
pip install pandas==2.2.3 numpy==1.23.1 scikit-learn==1.2.2 matplotlib seaborn scipy==1.9.0
```

4. **Run the Python script**
```bash
python customer_segmentation/scripts/segmentation.py
```

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

3. A file named `customer_segments.csv` should be saved under:
   ```
   /customer_segmentation/
   ```

---

## Output Summary

### 1. `customer_segments.csv`

This CSV file contains:
- `Customer_ID`: The unique customer identifier
- `Segment`: Assigned segment label for each customer

Segmentation is done using the **KMeans algorithm**, based on customer behavioural features such as balance and transaction frequency.

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

