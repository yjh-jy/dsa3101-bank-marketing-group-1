# Campaign Optimization

This documentation provides step-by-step instructions for setting up a real-time customer segmentation model locally using Kafka, PostgreSQL, and KMeans++, with simulated live transaction data for dynamic clustering and analysis.

## Prerequisites

Ensure that the following tools are installed on your machine:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

## Project Structure

Here’s a brief overview of the project structure:

```
/campaign_optimization 
│── /scripts                        # Backend scripts for data generation, ingestion, and optimization  
│   ├── /data_generation            # Real-time data generation scripts  
│   │   ├── real_time_data_generation.py   # Generates data every 5 seconds  
│   │   ├── Dockerfile                      # Dockerfile for the data generation script  
│   ├── /data_ingestion             # Real-time data ingestion scripts  
│   │   ├── real_time_data_ingestion.py    # Ingests Kafka data into Engagements table  
│   │   ├── Dockerfile                      # Dockerfile for the data ingestion script  
│   ├── campaign_optimization.py    # Populates the Thompson-Sampling model with data  
│   ├── data_ingestion_initial.py   # Loads initial dataset into Engagements table  
│  
│── /db                             # Database-related scripts  
│   ├── init_db.sql                 # Initializes PostgreSQL database schema  
│  
│── campaign_suggestion.py          # Recommends a campaign for a given segment  
│── docker-compose.yml              # Docker Compose configuration for containerized services  
│── README.md                       # Project documentation  
│── requirements.txt                # Python dependencies  
```

## Setup Instructions

Follow these steps to get the Kafka prototype running locally:

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine:

```bash
git clone <repository-url>
cd campaign_optimization
```
Here's the revised section with the Dash frontend integration:  

---

### 2. Running Services Sequentially  

#### Steps to Run the Services Sequentially  

1. **Build and Run Docker compose**  
   After pulling the repository, run the following command in your terminal to build the Docker image:  

   ```
    docker-compose down -v  # Removes containers AND volumes
    docker-compose up --build -d  # Rebuilds and starts fresh
   ```

2. **Run the Script:**  
   Now, run the script to build and start the services in the correct order:  

   ```
    run docker exec real_time_data python scripts/data_ingestion_initial.py
    run docker exec real_time_data python scripts/campaign_optimization.py
    run docker exec real_time_data python campaign_suggestion.py 
   ```
   
   run docker exec real_time_data python campaign_suggestion.py  is the main script to test which campaigns to recommend for a particular segment group. All you need to do is to adjust the global variables (INCOME_LEVEL, AGE_RANGE, MEDIA_TYPE)
 

### 3. PostgreSQL Integration  

This project integrates **PostgreSQL** as the primary database for handling customer segments and real-time transactions. The setup includes efficient data ingestion, batch processing, and automated updates using triggers and stored functions.  

The PostgresSQL db can be setup with the provided SQL script (`init_db.sql`).

### **Database Schema**  

#### **Tables**  

##### **`live_transaction_data`**  
Stores incoming transactions before aggregating them into `customer_segments`.  

| Column Name        | Data Type   | Description |
|-------------------|------------|-------------|
| `campaign_id`   | `INT` | Campaign ID |
| `income_category`     | `VARCHAR(50)` | Income cateogry of customer |
| `target_audience` | `VARCHAR(50)` | Age range of customer |
| `channel_used` | `VARCHAR(50)` | Channel of engagement used |
| `has_engaged` | `INT` | Indicates whether customer has engaged or not |

---

### 4. Verify the Setup

You can verify that everything is running correctly by checking the logs of the consumer and producer in split terminals:

```bash
docker-compose logs real_time_data -f
```

```bash
docker-compose logs real_time_data_ingestion -f
```

Look for messages indicating that both the producer and consumer are connected to Kafka and processing transactions.


### 6. Stopping the Services

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
