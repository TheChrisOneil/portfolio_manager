import os
import json
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.serialization import SimpleStringSchema


def recalculate_portfolio(transaction, current_prices, current_portfolios):
    """Update portfolio based on a transaction and market prices."""
    user = transaction['user']
    stock = transaction['stock']
    quantity = transaction['quantity'] if transaction['transaction_type'] == "buy" else -transaction['quantity']

    # Update portfolio quantities
    if user not in current_portfolios:
        current_portfolios[user] = {}
    current_portfolios[user][stock] = current_portfolios[user].get(stock, 0) + quantity

    # Calculate portfolio value using market prices
    portfolio_value = sum(
        quantity * current_prices.get(stock, 0)
        for stock, quantity in current_portfolios[user].items()
    )

    return {
        "user": user,
        "portfolio": current_portfolios[user],
        "total_value": portfolio_value
    }


def process_streams(transaction_json, market_json, portfolios_state, market_prices):
    """Main processing logic for transactions and market data."""
    try:
        # Update market prices
        if market_json:
            stock, price = market_json.split(":")
            market_prices[stock] = float(price)
            return None  # Market data doesn't produce an output directly

        # Process transactions
        if transaction_json:
            transaction = json.loads(transaction_json)
            updated_portfolio = recalculate_portfolio(transaction, market_prices, portfolios_state)
            return json.dumps(updated_portfolio)

    except Exception as e:
        print(f"Error processing stream: {e}")
        return None


def main():
    # Environment variables
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    transactions_topic = os.getenv("TRANSACTIONS_TOPIC", "user-transactions")
    market_data_topic = os.getenv("MARKET_DATA_TOPIC", "market-data")
    output_topic = os.getenv("OUTPUT_TOPIC", "portfolio-updates")
    group_id = os.getenv("GROUP_ID", "portfolio-recalculator")

    # Set up the Flink execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)

    # Kafka consumers
    transaction_source = FlinkKafkaConsumer(
        topics=transactions_topic,
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id
        }
    )
    market_source = FlinkKafkaConsumer(
        topics=market_data_topic,
        deserialization_schema=SimpleStringSchema(),
        properties={
            'bootstrap.servers': kafka_bootstrap_servers,
            'group.id': group_id
        }
    )

    # Kafka producer
    kafka_sink = FlinkKafkaProducer(
        topic=output_topic,
        serialization_schema=SimpleStringSchema(),
        producer_config={
            'bootstrap.servers': kafka_bootstrap_servers
        }
    )

    # In-memory state
    current_portfolios = {}
    market_prices = {}

    # Stream processing pipeline
    transaction_stream = env.from_source(transaction_source, "transaction-source", None)
    market_stream = env.from_source(market_source, "market-source", None)

    transaction_stream.union(market_stream) \
        .map(lambda data: process_streams(data if "transaction_type" in data else None,
                                          data if ":" in data else None,
                                          current_portfolios, market_prices)) \
        .filter(lambda x: x is not None) \
        .add_sink(kafka_sink)

    # Execute the Flink job
    env.execute("Portfolio Recalculator with Market Data")


if __name__ == "__main__":
    main()
