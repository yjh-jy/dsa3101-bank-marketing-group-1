# Segmentation Updates

This module is designed to provide hands-on experience with real-time customer segmentation using modern data engineering tools. The system leverages **Kafka, PostgreSQL, and KMeans++** to process live transaction data, dynamically clustering customers based on their financial behavior and engagement patterns. Additionally, it includes a **Dash frontend** for real-time visualization of segmentation results.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Clone the Repository](#1-clone-the-repository)
  - [Start Services in the Correct Order](#2-start-services-in-the-correct-order)
  - [Verify the Setup](#3-verify-the-setup)
  - [Access Real-Time Visualization](#4-access-real-time-visualization)
  - [Stop Services](#5-stop-services)
- [Database Schema](#database-schema)
- [Troubleshooting](#troubleshooting)

---
## Prerequisites

Ensure the following dependencies are installed before running the system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

---
## Project Structure

```
/segmentation-updates
    /api                            # Dash frontend and Flask API
        app.py                      # Entry point for the visualization dashboard
        Dockerfile                  # Dockerfile for the frontend
    /consumer                       # Kafka consumer service
        consumer.py                 # Kafka consumer script
        Dockerfile                  # Consumer container setup
    /db                             # Database initialization
        init_db.sql                 # SQL script to create required tables
    /producer                       # Kafka producer service
        producer.py                 # Kafka producer script
        Dockerfile                  # Producer container setup
    build_and_start.sh              # Automates container build and startup
    customer_segments_full.csv      # Seed data for database initialization
    docker-compose.yml              # Orchestration file for services
    requirements.txt                # Python dependencies
    README.md                       # Documentation
```

---
## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd segmentation_updates
```

### 2. Start Services in the Correct Order

To ensure proper dependencies, use the provided startup script:

```bash
chmod +x build_and_start.sh
./build_and_start.sh
```

**Service Order:**
1. **Zookeeper** (Manages Kafka brokers)
2. **Kafka** (Message broker for event streaming)
3. **PostgreSQL** (Database backend for customer segments)
4. **Kafka Producer** (Generates synthetic transaction data)
5. **Kafka Consumer** (Processes data and updates customer segments)
6. **Dash Frontend** (Visualizes segmentation results)

Once all services are running, you should see logs indicating successful Kafka and PostgreSQL connections.

### 3. Verify the Setup

Monitor logs to ensure all services are functioning correctly:

```bash
docker-compose logs producer -f
docker-compose logs consumer -f
docker-compose logs segmentation_service -f
```

### 4. Access Real-Time Visualization

Once running, access the dashboard at:

```
http://localhost:5001/dashboard/
```

**Dashboard Features:**
- **Real-Time Data Updates:** Transactions processed dynamically.
- **Scatter Plot:** Visualizes customer clusters based on financial attributes.
- **Sorted Table:** Lists customers with their assigned segments and other attributes based on `latest_updated`

### 5. Stop Services

```bash
docker-compose down
```

---
## Database Schema

### `customer_segments` Table
Stores the aggregated customer from `customer_segmentation` sub-project and updates dynamically based on transactions.

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

1. **Kafka/Zookeeper Startup Failure:**
A key consideration is that running `docker-compose up -d` may not work as expected because Kafka services take time to initialize. If the producer or consumer starts before Kafka is fully ready, it can result in a "Kafka broker not found" error. To avoid this, use the provided `build_and_start.sh` script, which ensures services are started in the correct sequence.

   - Ensure Docker is running and check which service exited
     ```bash
     docker ps -a
     ```
     
   - Check logs for errors:
     ```bash
     docker-compose logs kafka -f
     ```

3. **Database Not Connecting:**
   - Verify PostgreSQL container is running:
     ```bash
     docker ps | grep postgres
     ```
   - Manually restart database service:
     ```bash
     docker-compose restart postgres
     ```

4. **Port Conflicts:**
   - Ensure no other services are running on conflicting ports (Zookeeper: `2181`, Kafka: `9092`, PostgreSQL: `5432`, Dash API: `5001`).

5. **Transaction ID Conflicts:**
   - Clear database volumes (local development only):
     ```bash
     docker volume rm segmentation_updates_postgres_data
     ```

For persistent issues, check system resource limits and increase Docker memory allocation if necessary.

---
## Contributing

If you'd like to contribute, please fork the repository and submit a pull request with your improvements or feature enhancements.

