from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os

app = Flask(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

@app.route('/produce', methods=['POST'])
def produce_message():
    content = request.json
    topic = content.get('topic')
    message = content.get('message')

    if not topic or not message:
        return jsonify({'error': 'Invalid payload'}), 400

    producer.send(topic, value=message)
    producer.flush()

    return jsonify({'status': 'Message sent'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

