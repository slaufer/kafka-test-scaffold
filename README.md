### README

# Kafka Test Scaffold

This project provides a scaffold for testing Kafka consumers. It includes a containerized Kafka setup with Zookeeper, Kafka broker, and an HTTP API that sends messages to Kafka topics. The setup is designed to be used by developers who are writing Kafka consumers and want to test their implementations in a local environment.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**

   ```sh
   git clone <repository_url>
   cd kafka-test-scaffold
   ```

2. **Create a `topics.conf` file to define the Kafka topics:**

   ```sh
   echo "test" > topics.conf
   ```

3. **Start the services:**

   ```sh
   ./startup.sh
   ```

   This script will:
   - Build and start the Docker services.
   - Wait for Kafka to be ready.
   - Create the Kafka topics defined in `topics.conf`.

4. **Send a POST request to the API to produce a message to Kafka:**

   ```sh
   curl -X POST http://localhost:5000/produce -H "Content-Type: application/json" -d '{"topic": "test", "message": {"key": "value"}}'
   ```

   Example output:
   ```json
   {"status":"Message sent"}
   ```

5. **Consume the message using `kafkacat`:**

   ```sh
   kafkacat -b localhost:9094 -t test -C -o beginning
   ```

   Example output:
   ```json
   {"key": "value"}
   % Reached end of topic test [0] at offset 1
   ```

6. **Shut down the services:**

   ```sh
   ./shutdown.sh
   ```

   This script will stop and remove all Docker Compose services and volumes.

## Files

- `docker-compose.yml`: Defines the Docker services for Zookeeper, Kafka, and the HTTP API.
- `startup.sh`: Script to start the services, wait for Kafka to be ready, and create the Kafka topics.
- `shutdown.sh`: Script to stop and remove all Docker services and volumes.
- `app.py`: The HTTP API implementation that sends messages to Kafka.
- `topics.conf`: Configuration file to define Kafka topics.

## Notes

- The API continuously attempts to connect to Kafka until it succeeds, ensuring resilience to connection issues during startup.
- Ensure that Docker and Docker Compose are installed on your system before running the scripts.

This scaffold provides a simple way to test Kafka consumers by allowing you to produce messages to Kafka topics via an HTTP API and consume them through Kafka.
