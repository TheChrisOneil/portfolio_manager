# Use an official Flink image as the base
FROM apache/flink:1.16.0-scala_2.12

# Install Python, pip, and additional dependencies
RUN apt-get update && apt-get install -y python3 python3-pip \
    && pip3 install apache-flink \
    && pip3 install confluent-kafka \
    && pip3 install jsonschema \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python script and requirements
COPY ./src/flink/portfolio_recalculator.py /app/src/flink/
COPY ./src/flink/requirements.txt /app/

# Install Python dependencies from requirements.txt
RUN pip3 install -r /app/requirements.txt

# Set environment variables
ENV KAFKA_BOOTSTRAP_SERVERS="localhost:9092" \
    TRANSACTIONS_TOPIC="user-transactions" \
    MARKET_DATA_TOPIC="market-data" \
    OUTPUT_TOPIC="portfolio-updates" \
    GROUP_ID="portfolio-recalculator"
