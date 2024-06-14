from flask import Flask, request, jsonify
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient, TopicPartition
from kafka.admin import NewTopic
import json
import os
import time

app = Flask(__name__)

KAFKA_BOOTSTRAP_SERVERS = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')

def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return producer
        except Exception as e:
            print(f"Error connecting to Kafka: {e}")
            print("Retrying in 1 second...")
            time.sleep(1)

def create_kafka_admin():
    while True:
        try:
            admin = KafkaAdminClient(
                bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                client_id='kafka-admin'
            )
            return admin
        except Exception as e:
            print(f"Error connecting to Kafka Admin: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)

producer = create_kafka_producer()
admin_client = create_kafka_admin()

def create_topic(topic_name):
    try:
        topic_list = [NewTopic(name=topic_name, num_partitions=1, replication_factor=1)]
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
        print(f"Topic '{topic_name}' created.")
    except Exception as e:
        if 'TopicExistsError' not in str(e):
            print(f"Error creating topic '{topic_name}': {e}")
        else:
            print(f"Topic '{topic_name}' already exists.")

@app.route('/produce', methods=['POST'])
def produce_message():
    content = request.json
    topic = content.get('topic')
    message = content.get('message')

    if not topic or not message:
        return jsonify({'error': 'Invalid payload'}), 400

    create_topic(topic)
    
    producer.send(topic, value=message)
    producer.flush()

    return jsonify({'status': 'Message sent'}), 200

@app.route('/consume', methods=['GET'])
def consume_messages():
    topic = request.args.get('topic')
    if not topic:
        return jsonify({'error': 'Topic not specified'}), 400

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    messages = []
    partitions = consumer.partitions_for_topic(topic)
    if partitions is None:
        return jsonify({'error': 'Topic not found'}), 404

    for partition in partitions:
        tp = TopicPartition(topic, partition)
        consumer.assign([tp])
        consumer.seek_to_beginning(tp)

        while True:
            msg = consumer.poll(timeout_ms=1000)
            if not msg:
                break
            for record in msg.values():
                for message in record:
                    messages.append({
                        'topic': message.topic,
                        'partition': message.partition,
                        'offset': message.offset,
                        'key': message.key.decode('utf-8') if message.key else None,
                        'value': message.value
                    })
                    if message.offset == consumer.end_offsets([tp])[tp] - 1:
                        break

    consumer.close()
    return jsonify(messages)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

