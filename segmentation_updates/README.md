# Segmentation Updates

This module provides hands-on experience in real-time customer segmentation using modern data engineering tools. It leverages **Kafka** and **PostgreSQL** to process live transaction data, applying **KMeans++** to dynamically cluster customers based on their financial behavior and engagement patterns. A **Dash-powered frontend** enables real-time visualization of segmentation results, with **Flask** serving as the API entry point for GET requests.

---
## Project Structure

```
/segmentation-updates
    /api                            # Dash frontend and Flask API directory
        app.py                      # Entry point for the visualization dashboard
    /consumer                       # Kafka consumer directory
        consumer.py                 # Consumer script that consumes the incoming data, performs real-time clustering and updates the PostgresSQl db
    /db                             # Database initialization
        init_db.sql                 # SQL script to create required tables, triggers and upload inital data
    /producer                       # Kafka producer directory
        producer.py                 # Producer script that simulates live transactions
    customer_segments_full.csv      # Initial data for database initialization
    Dockerfile                      # Docker container setup
    README.md                       # Module-specific documentation
    requirements.txt                # Python dependencies
    run_scripts.sh                  # Bash script to coordinate all the script runs
```

---
## Setup Instructions

### 1. Ensure that the relevant docker services are up and running:

```bash
docker ps | grep postgres
docker ps | grep kafka
docker ps | grep zookeeper
docker ps | grep segmentation_updates
```

### 2. Run the bash script

To ensure proper dependencies, use the provided startup script:

```bash
./run_scripts.sh
```

### 3. Verify the Setup

Monitor logs to ensure that following outputs are logged correctly with no errors:

```bash
Running producer script....
Producer script started
Running consumer script....
Producer script started
Running Dash Frontend and Flask API script....
Dash Frontend and Flask API script started
All scripts ran for segmentation_updates
Please access the dashboard at:  http://localhost:5001/dashboard/
```

### 4. Access Real-Time Visualization

Once verified, access the dashboard at:

```
http://localhost:5001/dashboard/
```

**Dashboard Features:**
- **Real-Time Data Updates:** Transactions processed dynamically.
- **Scatter Plot:** Visualizes customer clusters based on financial attributes.
- **Sorted Table:** Lists customers with their assigned segments and other attributes based on `latest_updated`

### 5. Stop Service

```bash
docker container stop segmentation_updates
```

This will stop the main container serving the `producer.py`, `consumer.py` and `app.py` scripts.

Note that `campaign_optimization` depends on the same Kafka and Zookeeper containers so do not stop these two containers unless absolutely sure.

---
## Database Schema

### `customer_segments` Table
Stores the aggregated customer from `customer_segmentation` module and updates dynamically based on transactions.

| Column Name                  | Data Type   | Description |
|------------------------------|------------|-------------|
| `customer_id`                | `INT PRIMARY KEY` | Unique customer identifier |
| `income`                     | `FLOAT` | Annual income |
| `balance`                    | `FLOAT` | Current account balance |
| `customer_lifetime_value`     | `FLOAT` | Predicted value of the customer |
| `debt`                       | `FLOAT` | Outstanding debts |
| `tenure`                     | `INT` | Relationship duration (months) |
| `credit_default`             | `INT` | Whether the customer is in default or not (Boolean) |
| `days_from_last_transaction` | `INT` | Recency of last transaction |
| `avg_transaction_amt`        | `FLOAT` | Average transaction value |
| `num_transactions`           | `INT` | Total number of transactions |
| `digital_engagement_score`   | `FLOAT` | Engagement level metric |
| `total_products_owned`       | `INT` | Number of financial products owned |
| `transaction_freq`           | `FLOAT` | Transaction Frequency |
| `segment`                    | `VARCHAR(50)` | Customer segmentation label (Split into: High-Value, Budget-Conscious, At Risk / Inactive) |
| `last_updated`               | `TIMESTAMP` | Timestamp of last update |

### `live_transaction_data` Table
Captures real-time transactions before being processed into customer segments.

| Column Name       | Data Type  | Description |
|------------------|-----------|-------------|
| `transaction_id` | `INT PRIMARY KEY` | Unique transaction identifier |
| `customer_id`    | `INT` | Associated customer ID |
| `transaction_amt` | `FLOAT` | Transaction value |
| `transaction_time` | `TIMESTAMP` | Transaction timestamp |

---
## Troubleshooting

### Common Issues & Fixes

1. **Database Not Connecting:**
   - Verify PostgreSQL container is running:
     ```bash
     docker ps | grep postgres
     ```
     
2. **Port Conflicts:**
   - Ensure no other services are running on conflicting ports (Zookeeper: `2181`, Kafka: `9092`, PostgreSQL: `5432`, Dash API: `5001`).
  

For persistent issues, check system resource limits and increase Docker memory allocation if necessary.

---
## Contributing

If you'd like to contribute, please fork the repository and submit a pull request with your improvements or feature enhancements.
