# Kafka Test Scaffold

This project provides a scaffold for testing Kafka consumers. It includes a containerized Kafka setup with Zookeeper, Kafka broker, and an HTTP API that sends messages to Kafka topics and allows consuming messages from them. The setup is designed to be used by developers who are writing Kafka consumers and want to test their implementations in a local environment.

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

5. **Consume the messages using the `/consume` endpoint:**

   ```sh
   curl "http://localhost:5000/consume?topic=test"
   ```

   Example output:
   ```json
   [
       {
           "topic": "test",
           "partition": 0,
           "offset": 0,
           "key": null,
           "value": {"key": "value"}
       }
   ]
   ```

6. **Shut down the services:**

   ```sh
   docker-compose down -v
   ```

## Files

- `docker-compose.yml`: Defines the Docker services for Zookeeper, Kafka, and the HTTP API.
- `api/app.py`: The HTTP API implementation that sends messages to Kafka and creates topics on-the-fly if they don't already exist. It also provides an endpoint to consume Kafka messages.

## Notes

- The API continuously attempts to connect to Kafka until it succeeds, ensuring resilience to connection issues during startup.
- The API automatically creates Kafka topics on-the-fly if they don't already exist.
- Ensure that Docker and Docker Compose are installed on your system before running the commands.

