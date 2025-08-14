from fastapi import APIRouter, HTTPException
from services.producer import KafkaProducerService
from core.config import Settings

router = APIRouter(prefix="/producer", tags=["Producers"])
settings = Settings()
kafka_broker = settings.KAFKA_BROKER
producer_service = KafkaProducerService(kafka_broker)

@router.post("/start_producer/")
def start_producer(kafka_topic: str):
    """Starts the Kafka weather data producer."""
    response = producer_service.start_producer(kafka_topic)
    return response

@router.post("/stop_producer/")
def stop_producer():
    """Stops the Kafka weather data producer."""
    response = producer_service.stop_producer()
    return response
