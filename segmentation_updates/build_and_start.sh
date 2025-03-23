#!/bin/bash

# Step 1: Build and start the zookeeper service
echo "Building and starting Zookeeper service..."
docker-compose build zookeeper
docker-compose up -d zookeeper
echo "Zookeeper service started."

# Step 2: Build and start the Kafka service
echo "Building and starting Kafka service..."
docker-compose build kafka
docker-compose up -d kafka
echo "Kafka service started."

# Step 3: Build and start the Postgres service
echo "Building and starting consumer service..."
docker-compose build postgres
docker-compose up -d postgres
echo "Postgres service started."

# Step 4: Build and start the producer service
echo "Building and starting producer service..."
docker-compose build producer
docker-compose up -d producer
echo "Producer service started."

# Step 5: Build and start the api and dash service
echo "Building and starting consumer service..."
docker-compose build segmentation_service
docker-compose up -d segmentation_service
echo "Segmentation service (API and Dash) started."

# Step 6: Build and start the consumer service
echo "Building and starting consumer service..."
docker-compose build consumer
docker-compose up -d consumer
echo "Consumer service started."

echo "All services have been built and started successfully."