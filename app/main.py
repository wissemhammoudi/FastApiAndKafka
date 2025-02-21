from fastapi import FastAPI
from models.base import Base
from core.database import engine
import routers.topic, routers.producer,routers.consumer,routers.location,routers.weather

Base.metadata.create_all(engine)

app = FastAPI()

# Include Kafka routes
app.include_router(routers.topic.router)
app.include_router(routers.producer.router)
app.include_router(routers.consumer.router)
app.include_router(routers.location.router)
app.include_router(routers.weather.router)




@app.get("/")
def root():
    return {"message": "Kafka FastAPI service is running!"}
