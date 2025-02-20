from fastapi import APIRouter
from confluent_kafka import Consumer, KafkaError
from sqlalchemy import text
from models import Location, Weather
import json
import threading
from database import db_dependency
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from database import engine

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Kafka broker URL
KAFKA_BROKER = "broker:9092"

# Initialize router
router = APIRouter(prefix="/consamateur", tags=["Consamateur"])

consumer_thread = None  # Global thread variable
consumer_running = False


def store_weather_data_in_db(weather_data: dict):
    """Store the weather data into the PostgreSQL database."""
    db = SessionLocal()  # Create a new session
    try:
        # Step 1: Check if the location exists
        location_data = weather_data['location']
        location_name = location_data['name']
        location_country = location_data['country']

        location = db.query(Location).filter_by(name=location_name, country=location_country).first()

        # Step 2: If location doesn't exist, create a new Location
        if not location:
            location = Location(name=location_name, country=location_country)
            db.add(location)
            db.commit()  # Commit to save the new location
            db.refresh(location)  # Refresh to get the `location_id`

        # Step 3: Now create a new Weather entry linked to the location
        new_weather = Weather(
            location_id=location.location_id,
            observation_time=weather_data['observation_time'],
            temperature=weather_data['temperature'],
            weather_descriptions=weather_data['weather_descriptions'],
        )

        # Step 4: Add the weather data to the session and commit it
        db.add(new_weather)
        db.commit()
        print(f"✅ Stored weather data for location {location_name}, {location_country}")

    except SQLAlchemyError as e:
        db.rollback()
        print(f"❌ Error storing data: {e}")
    except Exception as e:
        db.rollback()
        print(f"❌ Unexpected error: {e}")
    finally:
        db.close()  # Close the session to avoid leaks


def run_consumer(kafka_topic: str):
    """Function to run the Kafka consumer."""
    global consumer_running
    consumer_running = True

    # Create a new consumer instance inside the function to avoid conflicts
    consumer = Consumer({
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': 'weather-consumer-group',
        'auto.offset.reset': 'earliest'
    })

    consumer.subscribe([kafka_topic])  # Subscribe to the given topic

    print(f"✅ Kafka consumer started for topic: {kafka_topic}")

    while consumer_running:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            print("⏳ No new messages received.")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print(f"🔚 End of partition reached: {msg.partition}")
            else:
                print(f"❌ Error consuming message: {msg.error()}")
        else:
            try:
                weather_data = json.loads(msg.value().decode('utf-8'))
                print(f"✅ Received message: {weather_data}")
                store_weather_data_in_db(weather_data)
            except Exception as e:
                print(f"❌ Error processing message: {e}")
        consumer.commit()

    consumer.close()  # Properly close the consumer
    print("❌ Kafka consumer stopped.")
    consumer_running = False


@router.post("/start_consumer/")
def start_consumer(kafka_topic: str):
    """Starts the Kafka consumer thread."""
    global consumer_thread, consumer_running

    if consumer_running:
        return {"message": "Kafka consumer is already running."}

    consumer_thread = threading.Thread(target=run_consumer, args=(kafka_topic,), daemon=True)
    consumer_thread.start()
    return {"message": f"Started consuming weather updates from Kafka topic '{kafka_topic}'"}


@router.get("/data/{table_name}", tags=["Database"])
def get_table_data(table_name: str, db: db_dependency = db_dependency):
    """Fetches all records from the given table."""
    query = text(f'SELECT * FROM "{table_name}"')
    result = db.execute(query)
    data = [dict(row) for row in result.mappings()]
    return {"table": table_name, "data": data}
