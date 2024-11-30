# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app


# Install required dependencies
RUN pip install confluent-kafka

# Set environment variables for runtime configuration
ENV KAFKA_BOOTSTRAP_SERVERS=""
ENV KAFKA_SASL_USERNAME=""
ENV KAFKA_SASL_PASSWORD=""

# Set the entry point to the Kafka producer script
CMD ["python", "/src/kafka/producer-market-data-sim.py"]
