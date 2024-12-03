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

# Copy Python script and dependencies
COPY ./src/flink/portfolio_recalculator.py /app/src/flink/

# Set environment variables
ENV APP_ROLE="" \
    APP_SCRIPT="" \
    KAFKA_BOOTSTRAP_SERVERS=""

# Default entry point for PyFlink
CMD ["python3", "/app/src/flink/portfolio_recalculator.py"]
