from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'a1e26f8e0b7c54805a12dc1e0ddffc44-1818854211.us-east-1.elb.amazonaws.com:9094',
    'group.id': 'test-consumer-group',
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
