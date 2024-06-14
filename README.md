# Kafka Test Scaffold

This project provides a scaffold for testing Kafka consumers. It includes a containerized Kafka setup with Zookeeper, Kafka broker, and an HTTP API that sends messages to Kafka topics. The setup is designed to be used by developers who are writing Kafka consumers and want to test their implementations in a local environment.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Clone the repository:**

   ```sh
   git clone git@github.com:slaufer/kafka-test-scaffold.git
   cd kafka-test-scaffold
   ```

2. **Build and Start the Docker Services:**

   ```sh
   docker-compose up --build
   ```

3. **Send a POST request to the API to produce a message to Kafka:**

   ```sh
   curl -X POST http://localhost:5000/produce -H "Content-Type: application/json" -d '{"topic": "test", "message": {"key": "value"}}'
   ```

   Example output:
   ```json
   {"status":"Message sent"}
   ```

4. **Consume the message using `kafkacat`:**

   ```sh
   kafkacat -b localhost:9094 -t test -C -o beginning
   ```

   Example output:
   ```
   {"key": "value"}
   % Reached end of topic test [0] at offset 1
   ```

5. **Shut down the services:**

   ```sh
   docker-compose down -v
   ```

## Files

- `docker-compose.yml`: Defines the Docker services for Zookeeper, Kafka, and the HTTP API.
- `app.py`: The HTTP API implementation that sends messages to Kafka and automatically creates topics if they don't already exist.

## Notes

- The API continuously attempts to connect to Kafka until it succeeds, ensuring resilience to connection issues during startup.
- The API automatically creates Kafka topics on-the-fly if they don't already exist.
- Ensure that Docker and Docker Compose are installed on your system before running the commands.

This scaffold provides a simple way to test Kafka consumers by allowing you to produce messages to Kafka topics via an HTTP API.

