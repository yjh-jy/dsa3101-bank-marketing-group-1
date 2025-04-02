# Campaign Optimization

This documentation provides step-by-step instructions for setting up a campaign optimization model locally using Kafka, PostgreSQL, and Thmompson-Sampling.

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
│   ├── /data_ingestion             # Real-time data ingestion scripts  
│   │   ├── real_time_data_ingestion.py    # Ingests Kafka data into Engagements table  
│   ├── campaign_optimization.py    # Populates the Thompson-Sampling model with data  
│   ├── data_ingestion_initial.py   # Loads initial dataset into Engagements table  
│  
│── /db                             # Database-related scripts  
│   ├── init_db.sql                 # Initializes PostgreSQL database schema  
│  
│── campaign_suggestion.py          # Recommends a campaign for a given segment  
│── Dockerfile                      # Docker container setup
│── README.md                       # Module-specific documentation
│── requirements.txt                # Import required packages
└── run_scripts.sh                  # Bash script to coordinate all the script runs
```

## Setup Instructions

### 1. Ensure that the relevant docker services are up and running:

```bash
docker ps | grep postgres
docker ps | grep kafka
docker ps | grep zookeeper
docker ps | grep campaign_optimization
```

### 2. Run the bash script

To ensure proper dependencies, use the provided startup script and run it **twice**:

```bash
./run_scripts.sh
```

campaign_suggestion.py  is the main script to test which campaigns to recommend for a particular segment group. 

All you need to do is to adjust the global variables (INCOME_LEVEL, AGE_RANGE, MEDIA_TYPE)
 
### 3. PostgreSQL Integration  

This project integrates **PostgreSQL** as the primary database for handling engagements.

The PostgresSQL db can be setup with the provided SQL script (`init_db.sql`).

### **Database Schema**  

#### **Tables**  

##### **`engagements`**  
Stores incoming engagements to be utilized for measuring campaign optimization metrics.  

| Column Name        | Data Type   | Description |
|-------------------|------------|-------------|
| `campaign_id`   | `INT` | Campaign ID |
| `income_category`     | `VARCHAR(50)` | Income cateogry of customer |
| `target_audience` | `VARCHAR(50)` | Age range of customer |
| `channel_used` | `VARCHAR(50)` | Channel of engagement used |
| `has_engaged` | `INT` | Indicates whether customer has engaged or not |

---

### 4. Verify the Setup

Monitor logs to ensure that following outputs are logged correctly with no errors:

```bash
Starting analysis...
Starting real_time_data_generation.py ...
Starting real_time_data_ingestion.py ...
Starting data_ingestion_initial.py ...
Starting campaign_optimization.py ...
Starting campaign_suggestion.py ...
```
Additionally, the Most Selected Campaign will also be logged based on the suggestions given by the Multi-Bandit algorithm and as more data comes in, the Most Selected Campaign will change accordingly. 

To observe the change, run the following command to regenerate the suggestions:

```bash
docker exec -it campaign_optimization python campaign_suggestion.py income_level age_range media_type

e.g. docker exec -it campaign_optimization python campaign_suggestion.py "High Income" "25-34" "Google Ads"
```

#### Parameters:

INCOME_LEVEL: Choose from ['Low Income', 'Medium Income', 'High Income']
AGE_RANGE: Choose from ['18-24', '25-34', '35-44', '45-54', '55+']
MEDIA_TYPE: Choose from ['Google Ads', 'Telephone', 'Website', 'Email', 'TikTok', 'Instagram', 'Landline']

### 5. Stop Service

```bash
docker container stop campaign_optimization
```

This will stop the main container serving the `real_time_data_ingestion.py`, `real_time_data_generation.py`, `campaign_optimization.py` and `campaign_suggestion.py` scripts.

Note that `segmentation_updates` depends on the same Kafka and Zookeeper containers so do not stop these two containers unless absolutely sure.

## Troubleshooting

If you encounter any issues, try the following steps:
1. Ensure Docker are properly installed and running.
2. Check the logs for any error messages:

   ```bash
   docker-compose logs -f campaign_optimization
   docker-compose logs -f kafka
   docker-compose logs -f zookeeper
   docker-compose logs -f postgres
   ```