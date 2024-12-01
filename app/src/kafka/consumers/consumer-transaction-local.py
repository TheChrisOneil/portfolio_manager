import os
import json
from confluent_kafka import Consumer, KafkaException, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'a1e26f8e0b7c54805a12dc1e0ddffc44-1818854211.us-east-1.elb.amazonaws.com:9094',
    'group.id': 'test-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)

def process_message(msg):
    """Process the transaction message."""
    try:
        transaction = json.loads(msg.value().decode('utf-8'))
        print(f"Processing transaction: {transaction}")
    except Exception as e:
        print(f"Error processing message: {e}")

def consume_transactions():
    """Consume messages from the 'user-transactions' topic."""
    consumer.subscribe(['user-transactions'])

    try:
        print("Starting User Transactions Consumer...")
        while True:
            msg = consumer.poll(1.0)  # Wait for 1 second for a message

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event, ignore
                    continue
                else:
                    # Real error
                    raise KafkaException(msg.error())

            process_message(msg)

    except KeyboardInterrupt:
        print("Consumer interrupted.")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_transactions()
