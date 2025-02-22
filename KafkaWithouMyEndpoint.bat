@echo off

:: Step 1: Start Kafka container
echo Starting Kafka container...
docker run -d --name=kafka -p 9092:9092 apache/kafka
timeout /t 10

:: Step 2: Verify the Kafka cluster is running
echo Verifying Kafka cluster...
docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092

:: Step 3: Produce messages to a topic
echo Producing messages to the topic "demo"...
docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic demo

:: Step 4: Consume messages from the topic
echo Consuming messages from the topic "demo"...
docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic demo --from-beginning

:: End
echo Kafka operations complete.
pause
