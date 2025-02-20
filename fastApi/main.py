from fastapi import FastAPI
from models import Base
from database import engine
import routers.topicroutes, routers.producerrouters,routers.consmerroutes

Base.metadata.create_all(engine)

app = FastAPI()

# Include Kafka routes
"""app.include_router(kafka_router, prefix="/kafka")"""
app.include_router(routers.topicroutes.router, prefix="/topic")
app.include_router(routers.producerrouters.router, prefix="/producer")
app.include_router(routers.consmerroutes.router, prefix="/consumer")



@app.get("/")
def root():
    return {"message": "Kafka FastAPI service is running!"}
