# routers/weather_router.py
from fastapi import APIRouter, Depends
from services.consumer import KafkaConsumerService
import threading
from dependencies.database import db_dependency
from core.config import Settings

router = APIRouter(prefix="/consumer", tags=["consumer"])
settings = Settings()
kafka_broker = settings.KAFKA_BROKER
kafka_service=KafkaConsumerService(kafka_broker,db_dependency)

@router.post("/start_consumer/")
def start_consumer(kafka_topic: str):
    """Starts the Kafka consumer thread."""
    def consumer_thread():
        start_consumer(kafka_topic)
    threading.Thread(target=consumer_thread, daemon=True).start()
    return {"message": f"Started consuming weather updates from Kafka topic '{kafka_topic}'"}
