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
    'bootstrap.servers': 'a1e26f8e0b7c54805a12dc1e0ddffc44-1818854211.us-east-1.elb.amazonaws.com:9094',
    'group.id': 'test-consumer-group',
    'auto.offset.reset': 'earliest'
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
