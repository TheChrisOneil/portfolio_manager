# Use the Flink image
FROM flink:1.16.0-scala_2.12

# Set working directory
WORKDIR /app

# Copy the compiled JAR file
COPY PortfolioRecalculator.jar /app/PortfolioRecalculator.jar

# Entry point for Flink
ENTRYPOINT ["flink", "run", "-c", "PortfolioRecalculator", "/app/PortfolioRecalculator.jar"]
