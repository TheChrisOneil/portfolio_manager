# Use an official Flink image as the base
FROM apache/flink:1.16.0-scala_2.12

# Install PyFlink and any additional dependencies
RUN pip install apache-flink \
    && pip install confluent-kafka \
    && pip install jsonschema  # Add any additional libraries as required

# Set working directory
WORKDIR /app

# Copy Python script and dependencies
COPY ./src/flink/portfolio_recalculator.py /app/src/flink/

# Set environment variables
ENV APP_ROLE="" \
    APP_SCRIPT="" \
    KAFKA_BOOTSTRAP_SERVERS=""

# Default entry point for PyFlink
CMD ["python", "/app/src/flink/portfolio_recalculator.py"]
