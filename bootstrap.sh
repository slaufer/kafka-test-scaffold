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

# Clean up any existing containers
echo "Cleaning up existing containers..."
docker-compose down -v

# Build and start the Docker services
echo "Building and starting Docker services..."
docker-compose up --build -d

# Wait for Kafka to be ready
echo "Waiting for Kafka to be ready..."
sleep 20

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
        docker-compose exec kafka kafka-topics --create --topic "$topic" --bootstrap-server localhost:9093 --replication-factor 1 --partitions 1
        echo "Topic '$topic' created."
    fi
done < "$TOPICS_FILE"

echo "Setup complete. Kafka is running and topics are created."

