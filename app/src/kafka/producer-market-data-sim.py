import os
import json
import random
import time
from datetime import datetime
from confluent_kafka import Producer

# List of NASDAQ companies (shortened for brevity)
nasdaq_companies = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA"]

# Kafka producer configuration
conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv('KAFKA_SASL_USERNAME'),
    'sasl.password': os.getenv('KAFKA_SASL_PASSWORD'),
    'client.id': 'nasdaq-simulator-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Delivered to {msg.topic()} [{msg.partition()}]")

def generate_market_data():
    while True:
        company = random.choice(nasdaq_companies)
        data = {
            "symbol": company,
            "price": round(random.uniform(100, 1000), 2),
            "volume": random.randint(1000, 100000),
            "timestamp": datetime.utcnow().isoformat()
        }
        producer.produce('market_data', value=json.dumps(data), callback=delivery_report)
        producer.poll(0)
        time.sleep(random.uniform(0.1, 1))

if __name__ == "__main__":
    try:
        print("Starting NASDAQ Market Data Producer...")
        generate_market_data()
    except KeyboardInterrupt:
        print("Shutting down producer.")
    finally:
        producer.flush()
