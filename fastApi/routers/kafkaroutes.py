from fastapi import APIRouter, HTTPException
from confluent_kafka import KafkaException, Producer,Consumer,KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
"""import httpx"""
from sqlalchemy import text
from models import Location,Weather
import time
import json
import threading
from database import db_dependency
from sqlalchemy.exc import SQLAlchemyError
import random
from datetime import datetime
# Kafka broker URL
KAFKA_BROKER = "broker:9092"

# Initialize router
router = APIRouter()

"""WEATHER_API_KEY = "82fa3bf102a0cf720fada7ad138fd8d1"  
BASE_URL = "http://api.weatherstack.com/current"""
producer_task = None
consumer_thread = None  # Global thread variable
consumer_running = False 
# Initialize Kafka Producer
producer = Producer({'bootstrap.servers': KAFKA_BROKER})
consumer = Consumer({
    'bootstrap.servers': KAFKA_BROKER,  # replace with actual Kafka broker address
    'group.id': 'weather-consumer-group',
    'auto.offset.reset': 'earliest',  # To start reading from the beginning if no offsets are stored
})


"""def fetch_weather(location: str):
    params = {"access_key": WEATHER_API_KEY, "query": location, "units": "m"}
    response = httpx.get(BASE_URL, params=params)

    if response.status_code != 200:
        return None

    data = response.json()
    if "error" in data:
        return None

    return data
"""



def consume_weather_data(kafka_topic: str):
    """Consume weather data from Kafka and store it in the database."""
    consumer.subscribe(kafka_topic)
    while True:
        msg = consumer.poll(timeout=1.0)  # Poll for new messages
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"End of partition reached: {msg.partition}")
            else:
                print(f"Error consuming message: {msg.error()}")
        else:
            try:
                weather_data = json.loads(msg.value().decode('utf-8'))
                store_weather_data_in_db(weather_data,db_dependency)
            except Exception as e:
                print(f"Error processing message: {e}")
        consumer.commit()  



def store_weather_data_in_db(weather_data: dict, db: db_dependency):
    """Store the weather data into the PostgreSQL database."""
    try:
        # Step 1: Check if the location exists
        location_data = weather_data['location']
        location_name = location_data['name']
        location_country = location_data['country']

        location = db.query(Location).filter_by(name=location_name, country=location_country).first()

        # Step 2: If location doesn't exist, create a new Location
        if not location:
            location = Location(
                name=location_name,
                country=location_country,
                region=location_data.get('region', 'Unknown'),
                lat=location_data.get('lat', 0.0),
                lon=location_data.get('lon', 0.0),
                timezone_id=location_data.get('timezone_id', 'UTC')
            )
            db.add(location)
            db.commit()  # Commit to save the new location
            db.refresh(location)  # Refresh to get the `location_id`

        # Step 3: Now create a new Weather entry linked to the location
        new_weather = Weather(
            location_id=location.location_id,
            observation_time=weather_data['current']['observation_time'],
            temperature=weather_data['current']['temperature'],
            weather_descriptions=weather_data['current']['weather_descriptions'],
            wind_speed=weather_data['current']['wind_speed'],
            wind_degree=weather_data['current']['wind_degree'],
            wind_dir=weather_data['current']['wind_dir'],
            pressure=weather_data['current']['pressure'],
            precip=weather_data['current']['precip'],
            humidity=weather_data['current']['humidity'],
            cloudcover=weather_data['current']['cloudcover'],
            feelslike=weather_data['current']['feelslike'],
            uv_index=weather_data['current']['uv_index'],
            visibility=weather_data['current']['visibility']
        )

        # Step 4: Add the weather data to the session and commit it
        db.add(new_weather)
        db.commit()

        print(f"Stored weather data for location {location_name}, {location_country}")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error storing data: {e}")
    except Exception as e:
        db.rollback()
        print(f"Unexpected error: {e}")



@router.get("/data/{table_name}", tags=["Database"])
def get_table_data(table_name: str, db:db_dependency):
    """Fetches all records from the given table."""
    if table_name not in ["Location", "weather"]:  # Restrict to specific tables
        return {"error": "Access to this table is not allowed"}
    
    query = text('SELECT * FROM "Weather"')
    result = db.execute(query)
    data = [dict(row) for row in result.mappings()]
    return {"table": table_name, "data": result}

def run_consumer(Kafka_Topic: list[str]):
    """Function to run the Kafka consumer."""
    global consumer_running
    consumer_running = True
    consume_weather_data(Kafka_Topic)
    consumer_running = False

@router.post("/start_consumer/")
def start_consumer(Kafka_Topic: list[str]):
    global consumer_thread, consumer_running

    if consumer_running:
        return {"message": "Kafka consumer is already running."}
    consumer_thread = threading.Thread(target=run_consumer, args=(Kafka_Topic,), daemon=True)
    consumer_thread.start()
    return {"message": f"Started consuming weather updates from Kafka topic '{Kafka_Topic}'"}
