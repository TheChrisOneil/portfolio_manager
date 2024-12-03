import os
import json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema


def recalculate_portfolio(transaction, current_portfolios):
    """Update portfolio based on a new transaction."""
    user_id = transaction['user_id']
    stock = transaction['stock']
    quantity = transaction['quantity']

    # Initialize the portfolio if it doesn't exist
    if user_id not in current_portfolios:
        current_portfolios[user_id] = {}

    # Update stock quantity
    current_portfolios[user_id][stock] = (
        current_portfolios[user_id].get(stock, 0) + quantity
    )

    return {user_id: current_portfolios[user_id]}


def process_transactions(transaction_json, portfolios_state):
    """Main processing logic for incoming transactions."""
    transaction = json.loads(transaction_json)
    updated_portfolio = recalculate_portfolio(transaction, portfolios_state)
    return json.dumps(updated_portfolio)


def main():
    # Load environment variables
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    input_topic = os.getenv("INPUT_TOPIC", "user-transactions")
    output_topic = os.getenv("OUTPUT_TOPIC", "user-portfolio")
    group_id = os.getenv("GROUP_ID", "portfolio-recalculator")

    # Set up the Flink execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)

    # Define Kafka source
    kafka_source = FlinkKafkaConsumer(
        topics=input_topic,
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id
        }
    )

    # Define Kafka sink
    kafka_sink = FlinkKafkaProducer(
        topic=output_topic,
        serialization_schema=SimpleStringSchema(),
        producer_config={
            'bootstrap.servers': kafka_bootstrap_servers
        }
    )

    # Current portfolios state (in-memory for simplicity)
    current_portfolios = {}

    # Stream processing
    env.from_source(kafka_source, "kafka-source", None) \
        .map(lambda x: process_transactions(x, current_portfolios)) \
        .add_sink(kafka_sink)

    # Execute the Flink job
    env.execute("Portfolio Recalculator")


if __name__ == "__main__":
    main()
