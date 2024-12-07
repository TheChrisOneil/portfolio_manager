from confluent_kafka import Consumer, KafkaException, KafkaError
import os
import json


def process_portfolio_update(message):
    """Process and display portfolio updates."""
    try:
        portfolio_update = json.loads(message)
        print(f"Portfolio Update: {json.dumps(portfolio_update, indent=4)}")
    except json.JSONDecodeError as e:
        print(f"Failed to decode message: {e}")
        print(f"Raw message: {message}")


def main():
    # Load environment variables or set defaults
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    topic = os.getenv("OUTPUT_TOPIC", "portfolio-updates")
    group_id = os.getenv("GROUP_ID", "portfolio-consumer")

    # Kafka consumer configuration
    consumer_config = {
        'bootstrap.servers': kafka_bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',  # Start reading at the earliest message
    }

    # Create the Kafka consumer
    consumer = Consumer(consumer_config)

    # Subscribe to the topic
    consumer.subscribe([topic])

    print(f"Consuming messages from topic: {topic}")

    try:
        while True:
            # Poll for a message
            msg = consumer.poll(1.0)  # Timeout in seconds

            if msg is None:
                continue  # No message received
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"End of partition reached: {msg.error()}")
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                # Process the message
                process_portfolio_update(msg.value().decode('utf-8'))
    except KeyboardInterrupt:
        print("Shutting down consumer...")
    finally:
        # Close the consumer
        consumer.close()


if __name__ == "__main__":
    main()
