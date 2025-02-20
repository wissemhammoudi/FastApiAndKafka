from fastapi import APIRouter, HTTPException
from confluent_kafka.admin import AdminClient,NewTopic
from confluent_kafka import KafkaException
# Initialize router
router = APIRouter(prefix="/topic", tags=["Topics"])
KAFKA_BROKER = "broker:9092"

@router.post("/create_topic")
def create_topic(topic_name: str, num_partitions: int = 1, replication_factor: int = 1):
    """Creates a Kafka topic dynamically with user-defined partitions and replication factor."""
    if not topic_name.strip():
        raise HTTPException(status_code=422, detail="Topic name cannot be empty.")
    if num_partitions < 1:
        raise HTTPException(status_code=422, detail="Number of partitions must be at least 1.")
    if replication_factor < 1:
        raise HTTPException(status_code=422, detail="Replication factor must be at least 1.")

    admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
    topic_list = [NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)]

    try:
        futures = admin_client.create_topics(topic_list)
        for topic, future in futures.items():
            future.result(timeout=30)  # Wait for topic creation
        return {
            "message": f"Topic '{topic_name}' created successfully",
            "partitions": num_partitions,
            "replication_factor": replication_factor
        }
    except KafkaException as e:
        raise HTTPException(status_code=500, detail=f"Kafka error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.get("/topics")
def list_topics():
    """Fetches all Kafka topics available in the broker."""
    try:
        admin_client = AdminClient({'bootstrap.servers': KAFKA_BROKER})
        topic_metadata = admin_client.list_topics(timeout=10)
        topics = list(topic_metadata.topics.keys())
        return {"topics": topics}
    except KafkaException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching topics: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
