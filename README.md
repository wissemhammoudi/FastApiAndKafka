# Event_Driven_Data_Ingestion
Start a kafka container by running the following command :
docker run -d --name=kafka -p 9092:9092 apache/kafka
The apache/kafka image ships with several helpful scripts in the /opt/kafka/bin directory.

Run the following command to verify the cluster is up and running and get its cluster ID:
docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server :9092

Create a sample topic and produce (or publish) a few messages by running the following command:
docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo

After running, you can enter a message per line


Confirm the messages were published into the cluster by consuming the messages:

docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server :9092 --topic demo --from-beginning
