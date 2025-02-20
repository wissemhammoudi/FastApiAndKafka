from fastapi import APIRouter
from confluent_kafka import Producer
import time
import json
import threading
import random
from datetime import datetime


# Kafka broker URL
KAFKA_BROKER = "broker:9092"
producer_task = None

router = APIRouter(prefix="/producer", tags=["Producers"])
producer = Producer({'bootstrap.servers': KAFKA_BROKER})

def generate_weather_data():
    """
    Generates random weather data.
    """
    # List of potential cities and countries
    cities = [
        {"name": "New York", "country": "USA"},
        {"name": "London", "country": "UK"},
        {"name": "Paris", "country": "France"},
        {"name": "Berlin", "country": "Germany"},
        {"name": "Tokyo", "country": "Japan"},
    ]
    
    # Randomly select a city
    selected = random.choice(cities)
    
    # Create Location instance
    location_obj = {
        "name": selected["name"],
        "country": selected["country"]
    }
    
    # Create Weather instance
    weather_obj = {
        "observation_time": datetime.now().strftime("%H:%M:%S"),
        "temperature": random.randint(-10, 35),
        "weather_descriptions": random.choice([
            "Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"
        ]),
        "location": location_obj  # Embed location data
    }
    
    return weather_obj

def produce_weather_updates(kafka_topic: str):
    """Fetches weather data and sends it to Kafka every 10 seconds."""
    while producer_task:  # Use producer_task as the condition to stop
        weather_data = generate_weather_data()
        if weather_data:
            # Serialize the data to JSON
            serialized_data = json.dumps(weather_data)
            # Send to Kafka
            producer.produce(kafka_topic, value=serialized_data)
            producer.flush()  # Ensure message is sent
            print(f"Produced: {weather_data}")
        else:
            print("Failed to generate weather data.")
        
        # Wait for the specified interval
        time.sleep(10)

@router.post("/start_producer/")
def start_producer(kafka_topic: str):
    """Starts the Kafka weather data producer."""
    global producer_task
    if producer_task:
        return {"message": "Producer is already running"}

    # Start the producer loop in a separate thread
    producer_task = True
    threading.Thread(target=produce_weather_updates, args=(kafka_topic,), daemon=True).start()
    return {"message": f"Started producing weather updates for Kafka topic: {kafka_topic}"}

@router.post("/stop_producer/")
def stop_producer():
    """Stops the Kafka weather data producer."""
    global producer_task
    if producer_task:
        producer_task = False  # Set the producer_task to False to stop the loop
        return {"message": "Weather producer stopped successfully"}
    return {"message": "Producer is not running"}