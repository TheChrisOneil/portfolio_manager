# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the entire project to the container
COPY . /app

# Install dependencies (add flink TODO)
RUN pip install confluent-kafka 

# Set default environment variables for runtime configuration
ENV KAFKA_BOOTSTRAP_SERVERS=""
ENV KAFKA_CONSUMER_GROUP=""
ENV APP_ROLE=""
ENV APP_SCRIPT=""
ENV FLINK_JOB=""

# Generic entry point for all roles
CMD ["sh", "-c", "\
    case \"$APP_ROLE\" in \
      producer) \
        if [ -z \"$APP_SCRIPT\" ]; then echo 'Missing APP_SCRIPT for producer role' && exit 1; fi; \
        if [ ! -f \"/app/src/kafka/producers/$APP_SCRIPT\" ]; then echo \"Producer script /app/src/kafka/producers/$APP_SCRIPT does not exist\" && exit 1; fi; \
        python /app/src/kafka/producers/$APP_SCRIPT; \
        ;; \
      consumer) \
        if [ -z \"$APP_SCRIPT\" ]; then echo 'Missing APP_SCRIPT for consumer role' && exit 1; fi; \
        if [ ! -f \"/app/src/kafka/consumers/$APP_SCRIPT\" ]; then echo \"Consumer script /app/src/kafka/consumers/$APP_SCRIPT does not exist\" && exit 1; fi; \
        python /app/src/kafka/consumers/$APP_SCRIPT; \
        ;; \
      flink) \
        if [ -z \"$FLINK_JOB\" ]; then echo 'Missing FLINK_JOB for flink role' && exit 1; fi; \
        if [ ! -f \"/app/src/flink/$FLINK_JOB\" ]; then echo \"Flink job /app/src/flink/$FLINK_JOB does not exist\" && exit 1; fi; \
        flink run /app/src/flink/$FLINK_JOB; \
        ;; \
      *) \
        echo 'Invalid APP_ROLE specified. Must be producer, consumer, or flink.' && exit 1; \
        ;; \
    esac"]
