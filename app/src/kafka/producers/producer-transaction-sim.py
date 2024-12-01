import os
import json
import random
import time
from datetime import datetime
from confluent_kafka import Producer

# List of NASDAQ companies (stocks)
nasdaq_companies = ["AAPL", "MSFT", "AMZN", "GOOG", "TSLA"]

# Simulated users
users = ["user1", "user2", "user3", "user4"]

# Kafka producer configuration
conf = {
    'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS", "my-cluster-kafka-bootstrap:9092"),
    'client.id': 'user-transactions-producer',
}

producer = Producer(conf)

def delivery_report(err, msg):
    """Callback for message delivery reports."""
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

def generate_transactions():
    """Simulate user transactions."""
    while True:
        # Randomly pick a user and stock
        user = random.choice(users)
        stock = random.choice(nasdaq_companies)

        # Randomly generate a transaction type (buy/sell) and quantity
        transaction_type = random.choice(["buy", "sell"])
        quantity = random.randint(1, 100)  # Quantity range: 1 to 100

        # Create the transaction message
        transaction = {
            "user": user,
            "stock": stock,
            "transaction_type": transaction_type,
            "quantity": quantity,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Send the message to the Kafka topic
        producer.produce('user-transactions', value=json.dumps(transaction), callback=delivery_report)

        # Poll to handle message delivery reports
        producer.poll(0)

        # Simulate delay between transactions
        time.sleep(random.uniform(0.5, 2))  # Delay of 0.5 to 2 seconds

if __name__ == "__main__":
    try:
        print("Starting User Transactions Producer...")
        generate_transactions()
    except KeyboardInterrupt:
        print("Shutting down producer.")
    finally:
        producer.flush()
