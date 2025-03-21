# Segmentation Updates
This documentation provides step-by-step instructions for running a basic Kafka prototype locally using Docker.

## Prerequisites

Ensure that the following tools are installed on your machine:
- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Python 3.10.6**: [Install Python](https://www.python.org/downloads/)

## Project Structure

Here’s a brief overview of the project structure:

```
/segmentation-updates
    /docker-compose.yml      # Docker Compose configuration to run the containers
    /producer                # Directory containing producer.py script
        producer.py          # Kafka producer script
        Dockerfile           # Dockerfile for the producer
    /consumer                # Directory containing consumer.py script
        consumer.py          # Kafka consumer script
        Dockerfile           # Dockerfile for the consumer
    /requirements.txt        # Python dependencies for Docker
    /build_and_start.sh      # Bash script to coordinate container builds and runs
    /init_db.sql             # Optional SQL script for initializing the PostgreSQL DB
    /other_folders_scripts   # Optional eda scripts or model scripts
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
- **Producer** starts once Kafka is operational, and it can begin producing messages to Kafka.
- **Consumer** starts last, after Kafka is ready to handle incoming messages.

By following this order, you ensure that all services are started in the correct sequence, allowing them to function properly together.

Kafka will be running on your local machine, and the producer and consumer will simulate transactions in real-time.

### 3. Verify the Setup

You can verify that everything is running correctly by checking the logs:

```bash
docker-compose logs -f
```

Look for messages indicating that both the producer and consumer are connected to Kafka and processing transactions.

### 4. PostgreSQL (Optional)

A PostgreSQL database is provided as part of the setup with a basic SQL script (`init_db.sql`). If you don't need the PostgreSQL setup, you can remove or modify the configuration in `docker-compose.yml` and the SQL file. 

To initialize the database, uncomment out and ensure the PostgreSQL service is running in your `docker-compose.yml`, then use the following command to check the logs for the database setup:

```bash
docker-compose logs -f postgres
```

### 4. Stopping the Services

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

## Notes

- The PostgreSQL database setup is optional and may be removed in future versions if found unnecessary.
- The producer and consumer scripts can be modified to handle different types of data or additional functionality.
