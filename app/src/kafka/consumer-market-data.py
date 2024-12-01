import os
from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group.id': os.getenv('KAFKA_CONSUMER_GROUP', 'test-consumer-group'),
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['market_data'])

print("Consuming messages from Kafka...")
try:
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Error: {msg.error()}")
        else:
            print(f"Received message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    consumer.close()

