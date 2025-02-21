from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import KafkaException
from typing import Optional

class KafkaTopicService:
    def __init__(self, kafka_broker: str):
        self.kafka_broker = kafka_broker

    def create_topic(self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1,
                     retention_ms: Optional[int] = None, retention_bytes: Optional[int] = None):
        """Creates a Kafka topic dynamically with user-defined partitions, replication factor, and retention policies."""
        if not topic_name.strip():
            raise ValueError("Topic name cannot be empty.")
        if num_partitions < 1:
            raise ValueError("Number of partitions must be at least 1.")
        if replication_factor < 1:
            raise ValueError("Replication factor must be at least 1.")

        # Build the configuration dictionary for topic-level settings
        config = {}
        if retention_ms is not None:
            config["retention.ms"] = str(retention_ms)
        if retention_bytes is not None:
            config["retention.bytes"] = str(retention_bytes)

        admin_client = AdminClient({'bootstrap.servers': self.kafka_broker})
        topic_list = [NewTopic(
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
            config=config
        )]

        try:
            futures = admin_client.create_topics(topic_list)
            for topic, future in futures.items():
                future.result(timeout=30)  # Wait for topic creation
            return {
                "message": f"Topic '{topic_name}' created successfully",
                "partitions": num_partitions,
                "replication_factor": replication_factor,
                "retention_policy": config
            }
        except KafkaException as e:
            raise Exception(f"Kafka error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

    def list_topics(self):
        """Fetches all Kafka topics available in the broker."""
        try:
            admin_client = AdminClient({'bootstrap.servers': self.kafka_broker})
            topic_metadata = admin_client.list_topics(timeout=10)
            topics = list(topic_metadata.topics.keys())
            return {"topics": topics}
        except KafkaException as e:
            raise Exception(f"Error fetching topics: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")
