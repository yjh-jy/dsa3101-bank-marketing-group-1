# Segmentation Updates
This documentation provides step-by-step instructions for setting up a real-time customer segmentation model locally using Kafka, PostgreSQL, and KMeans++, with simulated live transaction data for dynamic clustering and analysis.

## Prerequisites

Ensure that the following tools are installed on your machine:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

## Project Structure

Here’s a brief overview of the project structure:

```
/segmentation-updates
    /producer                       # Directory containing producer.py script
        producer.py                 # Kafka producer script
        Dockerfile                  # Dockerfile for the producer
    /consumer                       # Directory containing consumer.py script
        consumer.py                 # Kafka consumer script
        Dockerfile                  # Dockerfile for the consumer
    /db                             # Directory containing init_db.sql script
        init_db.sql                 # SQL script for initializing the PostgreSQL DB
    /build_and_start.sh             # Bash script to coordinate container builds and runs
    /customer_segments_full.csv     # Inital data for init_db.sql
    /docker-compose.yml             # Docker Compose configuration to run the containers
    /README.md                      # README documentation
    /requirements.txt               # Python dependencies for Docker
```

## Setup Instructions

Follow these steps to get the Kafka prototype running locally:

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd segmentation_updates
```

### 2. Running Services Sequentially

To ensure that the services are started in the correct order, a script (`build_and_start.sh`) is provided in the repository. This script automates the process of building and starting the services sequentially. This approach is important because some services depend on others to be fully operational before they can start. Specifically, **Zookeeper** must be up before **Kafka**, and **Kafka** must be running before the **Producer** and **Consumer** can interact with it.

#### Steps to Run the Services Sequentially

1. **Make the Script Executable:**
   After pulling the repository, make sure the `build_and_start.sh` script is executable. Run the following command in your terminal:

   ```bash
   chmod +x build_and_start.sh
   ```

2. **Run the Script:**
   Now, run the script to build and start the services in the correct order:

   ```bash
   ./build_and_start.sh
   ```

#### Why Run the Services in This Order?

- **Zookeeper** must be up and running before **Kafka** because Kafka relies on Zookeeper for managing cluster metadata and coordination. If Kafka starts before Zookeeper is ready, it will fail to initialize correctly.
- Once **Kafka** is running, the **Producer** can start sending data to Kafka, and the **Consumer** can begin consuming messages from Kafka.

Running the services sequentially ensures that each service is properly initialized and ready before the next service starts, minimizing the risk of service failures due to dependency issues.

#### Expected Outcome
- **Zookeeper** starts first, followed by **Kafka** once Zookeeper is ready.
- **Postgres** starts before **Consumer**, to ensure that the database is ready before insertion/update is executed
- **Producer** starts once Kafka is operational, and it can begin producing messages to Kafka.
- **Consumer** starts last, after Kafka is ready to handle incoming messages.

By following this order, you ensure that all services are started in the correct sequence, allowing them to function properly together.

Kafka and Postgres will be running on your local machine, and the producer and consumer will simulate transactions and clustering in real-time.

### 3. PostgreSQL Integration  

This project integrates **PostgreSQL** as the primary database for handling customer segments and real-time transactions. The setup includes efficient data ingestion, batch processing, and automated updates using triggers and stored functions.  

The PostgresSQL db can be setup with the provided SQL script (`init_db.sql`).

### **Database Schema**  

#### **Tables**  

##### **`customer_segments`**  
Stores customer information and dynamically updates clustering based on transaction history.  

| Column Name                    | Data Type    | Description |
|---------------------------------|-------------|-------------|
| `customer_id`                   | `INT PRIMARY KEY` | Unique identifier for each customer |
| `income`                        | `FLOAT`    | Annual income of the customer |
| `balance`                       | `FLOAT`    | Account balance |
| `customer_lifetime_value`       | `FLOAT`    | Predicted lifetime value of the customer |
| `debt`                          | `FLOAT`    | Outstanding debt |
| `tenure`                        | `INT`      | Duration of relationship with the company (years) |
| `credit_default`                | `INT`      | Indicates if the customer has defaulted on credit |
| `days_from_last_transaction`    | `INT`      | Number of days since last transaction |
| `avg_transaction_amt`           | `FLOAT`    | Average transaction amount (updated in real-time) |
| `num_transactions`              | `INT`      | Total transactions made |
| `digital_engagement_score`      | `FLOAT`    | Customer engagement score |
| `loan_repayment_time`           | `FLOAT`    | Estimated loan repayment time |
| `total_products_owned`          | `INT`      | Number of financial products owned |
| `has_loan`                      | `INT`      | Indicates if the customer has an active loan |
| `segment`                       | `VARCHAR(50)` | Customer segmentation label (updated dynamically) |
| `last_updated`                  | `TIMESTAMP`  | Timestamp for tracking last update |

##### **`live_transaction_data`**  
Stores incoming transactions before aggregating them into `customer_segments`.  

| Column Name        | Data Type   | Description |
|-------------------|------------|-------------|
| `transaction_id`   | `INT PRIMARY KEY` | Unique transaction ID |
| `customer_id`     | `INT` | Customer making the transaction |
| `transaction_amt` | `FLOAT` | Transaction amount |
| `transaction_time` | `TIMESTAMP` | Timestamp of the transaction |

---


### 4. Verify the Setup

You can verify that everything is running correctly by checking the logs of the consumer and producer in split terminals:

```bash
docker-compose logs consumer -f
```

```bash
docker-compose logs producer -f
```

Look for messages indicating that both the producer and consumer are connected to Kafka and processing transactions.

### 5. Stopping the Services

To stop all running services, use:

```bash
docker-compose down
```

This will stop the containers and remove the associated networks.

## Troubleshooting

If you encounter any issues, try the following steps:
1. Ensure Docker are properly installed and running.
2. Check the logs for any error messages:

   ```bash
   docker-compose logs
   ```

3. Make sure Kafka and Zookeeper are running correctly by verifying their logs.

4. Before starting a new instance, run `docker volume rm segmentation_updates_postgres_data` to remove persisted Postgres data. In production, this is not an issue because the producer runs continuously and does not restart, preventing conflicting transaction_id inserts. However, in our local setup, frequent restarts can lead to such conflicts.

## 📊 **Future Work: Real-Time Visualization**  

- Integrating a **dashboard** (e.g., **Streamlit, Dash, or Grafana**) to visualize customer segment changes in real-time.  
- Implementing a **web socket**-based system to push updates to the frontend dynamically.  
