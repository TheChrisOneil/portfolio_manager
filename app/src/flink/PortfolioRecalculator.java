import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.util.Collector;
import org.apache.flink.api.java.utils.ParameterTool;

import org.json.JSONObject;

import java.util.Properties;

public class PortfolioRecalculator {

    public static void main(String[] args) throws Exception {
        // Set up the execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Read parameters for Kafka configuration
        final ParameterTool params = ParameterTool.fromArgs(args);
        String kafkaBootstrapServers = params.get("kafka.bootstrap.servers", "my-cluster-kafka-bootstrap:9092");
        String inputTopic = params.get("input.topic", "user-transactions");
        String outputTopic = params.get("output.topic", "user-portfolio");

        // Set up Kafka consumer
        Properties consumerProps = new Properties();
        consumerProps.setProperty("bootstrap.servers", kafkaBootstrapServers);
        consumerProps.setProperty("group.id", "portfolio-recalculator");
        FlinkKafkaConsumer<String> kafkaConsumer = new FlinkKafkaConsumer<>(inputTopic, new SimpleStringSchema(), consumerProps);

        // Set up Kafka producer
        Properties producerProps = new Properties();
        producerProps.setProperty("bootstrap.servers", kafkaBootstrapServers);
        FlinkKafkaProducer<String> kafkaProducer = new FlinkKafkaProducer<>(outputTopic, new SimpleStringSchema(), producerProps);

        // Consume transactions from Kafka
        DataStream<String> transactions = env.addSource(kafkaConsumer);

        // Process transactions to recalculate the portfolio
        DataStream<String> recalculatedPortfolio = transactions
            .flatMap((String transaction, Collector<Tuple3<String, String, Integer>> out) -> {
                // Parse JSON transaction
                JSONObject json = new JSONObject(transaction);
                String user = json.getString("user");
                String stock = json.getString("stock");
                String transactionType = json.getString("transaction_type");
                int quantity = json.getInt("quantity");

                // Emit (user, stock, quantity change)
                int delta = transactionType.equalsIgnoreCase("buy") ? quantity : -quantity;
                out.collect(new Tuple3<>(user, stock, delta));
            })
            .returns(TypeInformation.of(Tuple3.class))
            .keyBy(t -> t.f0 + "-" + t.f1) // Group by user and stock
            .sum(2) // Aggregate quantity changes
            .map(tuple -> {
                // Convert aggregated data to JSON
                JSONObject json = new JSONObject();
                json.put("user", tuple.f0);
                json.put("stock", tuple.f1);
                json.put("quantity", tuple.f2);
                return json.toString();
            });

        // Write recalculated portfolio to Kafka
        recalculatedPortfolio.addSink(kafkaProducer);

        // Execute the Flink job
        env.execute("Portfolio Recalculator");
    }
}
