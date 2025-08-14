# routers/weather_router.py
from fastapi import APIRouter,Depends
from services.consumer import KafkaConsumerService
import threading
from dependencies.database import get_db
from core.config import Settings
from sqlalchemy.orm import Session


router = APIRouter(prefix="/consumer", tags=["consumer"])
settings = Settings()
kafka_broker = settings.KAFKA_BROKER

@router.post("/start_consumer/",response_model=None)
def start_consumer(kafka_topic: str, db: Session = Depends(get_db)):
    """Starts the Kafka consumer thread."""
    
    def consumer_thread():
        kafka_service = KafkaConsumerService(kafka_broker, db)
        kafka_service.start_consumer(kafka_topic)

    thread = threading.Thread(target=consumer_thread, daemon=True)
    thread.start()
    
    return {"message": f"Started consuming weather updates from Kafka topic '{kafka_topic}'"}
