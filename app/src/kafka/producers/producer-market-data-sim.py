import os
import random
import time
from confluent_kafka import Producer

# Fetch Kafka bootstrap server from environment variable
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

# Kafka Producer configuration
conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
}

# Create Kafka Producer instance
producer = Producer(conf)

# Callback for delivery report
def delivery_report(err, msg):
    """Callback for Kafka delivery reports."""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [partition {msg.partition()}]")

# Generate and send messages
print("Starting producer...")
nasdaq_companies = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA"]
try:
    while True:
        for company in companies:
            price = round(random.uniform(100, 500), 2)
            message = f"{company}: {price}"
            producer.produce("market_data", key=company, value=message, callback=delivery_report)
            time.sleep(1)  # Pause between messages for demonstration purposes
        
        producer.flush()
except KeyboardInterrupt:
    print("Producer stopped.")
finally:
    producer.flush()
