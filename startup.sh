#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Docker is installed
if ! command_exists docker; then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command_exists docker-compose; then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi

# Clean up any existing containers and volumes
echo "Cleaning up existing containers and volumes..."
docker-compose down -v

# Build and start the Docker services
echo "Building and starting Docker services..."
docker-compose up --build -d

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."

KAFKA_READY=false
while [ $KAFKA_READY == false ]; do
    docker-compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9094 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        KAFKA_READY=true
    else
        echo "Kafka is not ready yet, waiting..."
        sleep 1
    fi
done

# Read topics from configuration file
TOPICS_FILE="topics.conf"
if [ ! -f "$TOPICS_FILE" ]; then
    echo "Configuration file $TOPICS_FILE not found. Please create it and define your topics."
    exit 1
fi

# Create Kafka topics
echo "Creating Kafka topics..."
while IFS= read -r topic; do
    if [ -n "$topic" ]; then
        docker-compose exec -T kafka kafka-topics --create --topic "$topic" --bootstrap-server localhost:9094 --replication-factor 1 --partitions 1
        echo "Topic '$topic' created."
    fi
done < "$TOPICS_FILE"

echo "Setup complete. Kafka is running and topics are created."

