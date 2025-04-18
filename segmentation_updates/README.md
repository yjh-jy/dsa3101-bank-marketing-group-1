# Segmentation Updates

This module provides hands-on experience in real-time customer segmentation using modern data engineering tools. It leverages **Kafka** and **PostgreSQL** to process live transaction data, applying **KMeans++** to dynamically cluster customers based on their financial behavior and engagement patterns. A **Dash-powered frontend** enables real-time visualization of segmentation results, with **Flask** serving as the API entry point for GET requests.

---
## Project Structure

```
segmentation_updates/
├── api/                             # Dash frontend and Flask API directory
│   ├── app.py                       # Entry point for the visualization dashboard
├── consumer/                        # Kafka consumer directory
│   └── consumer.py                  # Consumer script that consumes the incoming data, performs real-time clustering and updates the PostgresSQl db
├── db/                              # Database directory
│   └── init_db.sql                  # SQL script to create required tables, triggers and upload inital data
├── producer/                        # Kafka producer directory
│   └── producer.py                  # Producer script that simulates live transactions
│── customer_segments_full.csv       # Initial data for database initialization
│── Dockerfile                       # Docker container setup
│── README.md                        # Module-specific documentation
│── requirements.txt                 # Import required packages
└── run_scripts.sh                   # Bash script to coordinate all the script runs
```

---
## Key Features
### **Kafka-Based Streaming Architecture**

Kafka is integrated as a message broker to enable real-time data flow, significantly improving responsiveness compared to traditional batch processing. Without Kafka, data ingestion and processing would rely on periodic updates, leading to delays in customer segmentation insights.

With Kafka, the system operates as follows:

- **Kafka Producer:** Publishes new transaction data to a Kafka topic instantly, eliminating batch delays and simulating real-time transaction data.
- **Kafka Broker:** Buffers and distributes messages with high throughput, preventing bottlenecks and ensuring seamless data streaming.
- **Kafka Consumer:** Continuously listens to transaction data, processes it using KMeans++ clustering in near real-time, and updates PostgreSQL.
- **Real-Time Updates:** The dashboard fetches the latest segmentation results from PostgreSQL, reflecting changes immediately rather than waiting for scheduled updates.

This setup ensures **scalability, low-latency processing, and fault tolerance**, making customer segmentation dynamic and responsive. Without Kafka, delays in data ingestion and processing would result in outdated insights, reducing the system's effectiveness in real-time decision-making.

### **Role of Relational Databases in Banking**

Banks rely on relational databases like PostgreSQL for secure, structured, and ACID-compliant data management. In this system:

- PostgreSQL ensures that transactional data integrity is maintained, preventing inconsistencies.
- Banks typically use relational databases to track account balances, fraud detection, and compliance reporting, where data accuracy is paramount.
- Kafka acts as a real-time data pipeline, feeding the latest transactions into PostgreSQL while ensuring rapid updates and historical tracking.
- By combining Kafka’s real-time capabilities with PostgreSQL’s structured querying, banks can dynamically segment customers and personalize offers based on up-to-date financial activity.

### **Interactive Visualization Dashboard**

Employs Dash to provide a quick prototype of a real-time interface for visualizing segmentation results, ensuring immediate insights into customer groupings as new transactions occur.

![Image](https://github.com/user-attachments/assets/de278577-0358-4145-9746-aee1e0fc2187)

Live View of the Dashboard

### **Modular Architecture**

Organized into distinct components—API, consumer, producer, and database directories—enhancing maintainability and scalability, with Kafka enabling efficient, real-time communication between them.

### **Future Extensions: Real-Time Clustering Algorithms**

Currently, the system uses KMeans++ for clustering, but more advanced real-time clustering algorithms could further enhance customer segmentation accuracy and adaptability. Potential extensions include:

- **Online KMeans:** Unlike traditional KMeans, this variant updates centroids incrementally, making it well-suited for continuously arriving transaction data.
- **Real-Time DBSCAN (RT-DBSCAN):** A density-based clustering method optimized for real-time processing, capable of detecting outliers and handling non-spherical data distributions efficiently. It has been applied in domains like fraud detection and real-time social media content analysis.

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

### 5. Stop Service

```bash
docker container stop segmentation_updates
```

This will stop the main container serving the `producer.py`, `consumer.py` and `app.py` scripts.

Note that `campaign_optimization` depends on the same Kafka and Zookeeper containers so do not stop these two containers unless absolutely sure.

---
## PostgresSQL Database Schema

### `customer_segments` Table
Stores the aggregated customer atttributes derived from the `customer_segmentation` module and updates dynamically based on transactions.

| Column Name                  | Data Type   | Description |
|------------------------------|------------|-------------|
| `customer_id`                | `INT PRIMARY KEY` | Unique customer identifier |
| `income`                     | `FLOAT` | Monthly income |
| `balance`                    | `FLOAT` | Average yearly balance |
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
