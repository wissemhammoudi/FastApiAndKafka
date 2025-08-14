from fastapi import APIRouter, HTTPException
from services.topic import KafkaTopicService
from core.config import Settings
from typing import Optional

router = APIRouter(prefix="/topic", tags=["Topics"])
settings = Settings()
kafka_broker = settings.KAFKA_BROKER
topic_service = KafkaTopicService(kafka_broker)

@router.post("/create_topic")
def create_topic(
    topic_name: str,
    num_partitions: int = 1,
    replication_factor: int = 1,
    retention_ms: Optional[int] = None,
    retention_bytes: Optional[int] = None
):
    """Creates a Kafka topic dynamically with user-defined partitions, replication factor, and retention policies."""
    try:
        return topic_service.create_topic(
            topic_name,
            num_partitions,
            replication_factor,
            retention_ms,
            retention_bytes
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
def list_topics():
    """Fetches all Kafka topics available in the broker."""
    try:
        return topic_service.list_topics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
