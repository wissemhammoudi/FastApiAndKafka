from confluent_kafka import Producer
import json
import time
import threading
from datetime import datetime
import random

class KafkaProducerService:
    def __init__(self, kafka_broker: str):
        self.kafka_broker = kafka_broker
        self.producer = None
        self.producer_task = None

    def generate_weather_data(self):
        """Generates random weather data."""
        cities = [
            {"name": "New York", "country": "USA"},
            {"name": "London", "country": "UK"},
            {"name": "Paris", "country": "France"},
            {"name": "Berlin", "country": "Germany"},
            {"name": "Tokyo", "country": "Japan"},
        ]
        selected = random.choice(cities)
        location_obj = {"name": selected["name"], "country": selected["country"]}
        weather_obj = {
            "observation_time": datetime.now().strftime("%H:%M:%S"),
            "temperature": random.randint(-10, 35),
            "weather_descriptions": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy", "Foggy", "Windy"]),
            "location": location_obj,
        }
        return weather_obj

    def produce_weather_updates(self, kafka_topic: str, sending_mode: str = "synchronous"):
        """Fetches weather data and sends it to Kafka every 10 seconds."""
        while self.producer_task:
            weather_data = self.generate_weather_data()
            if weather_data:
                serialized_data = json.dumps(weather_data).encode('utf-8')
                if sending_mode == "fire-and-forget":
                    self.producer.produce(kafka_topic, value=serialized_data)
                elif sending_mode == "synchronous":
                    self.producer.produce(kafka_topic, value=serialized_data)
                    self.producer.flush()
                elif sending_mode == "asynchronous":
                    def delivery_report(err, msg):
                        if err is not None:
                            print(f"Delivery failed for message {msg.value()}: {err}")
                        else:
                            print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    self.producer.produce(kafka_topic, value=serialized_data, callback=delivery_report)
                else:
                    print("Invalid sending mode specified.")
            else:
                print("Failed to generate weather data.")
            time.sleep(10)

    def start_producer(self, kafka_topic: str):
        """Starts the Kafka weather data producer."""
        if self.producer_task:
            return {"message": "Producer is already running"}
        # Initialize the producer here
        self.producer = Producer({'bootstrap.servers': self.kafka_broker})
        self.producer_task = True
        threading.Thread(target=self.produce_weather_updates, args=(kafka_topic,), daemon=True).start()
        return {"message": f"Started producing weather updates for Kafka topic: {kafka_topic}"}

    def stop_producer(self):
        """Stops the Kafka weather data producer."""
        if self.producer_task:
            self.producer_task = False
            # Ensure all messages are delivered before shutting down
            self.producer.flush()
            self.producer = None
            return {"message": "Weather producer stopped successfully"}
        return {"message": "Producer is not running"}
