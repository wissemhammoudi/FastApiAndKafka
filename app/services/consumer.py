from confluent_kafka import Consumer, KafkaError
from sqlalchemy.orm import Session
from models.location import Location
from models.weather import Weather
import json
from sqlalchemy.exc import SQLAlchemyError

class KafkaConsumerService:
    def __init__(self, kafka_broker: str, db: Session):
        self.kafka_broker = kafka_broker
        self.db = db
        self.consumer = None

    def start_consumer(self,kafka_topic:str):
        """Initialize and start the Kafka consumer."""
        self.consumer = Consumer({
            'bootstrap.servers': self.kafka_broker,
            'group.id': 'weather-consumer-group',
            'auto.offset.reset': 'earliest'
        })

        self.consumer.subscribe([kafka_topic])
        print(f"✅ Kafka consumer started for topic: {kafka_topic}")

        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        print(f"🔚 End of partition reached: {msg.partition()}")
                    else:
                        print(f"❌ Error consuming message: {msg.error()}")
                else:
                    self.process_message(msg)
        except Exception as e:
            print(f"❌ Exception in consumer loop: {e}")
        finally:
            self.consumer.close()
            print("❌ Kafka consumer stopped.")

    def process_message(self, msg):
        """Process and store the received Kafka message."""
        try:
            weather_data = json.loads(msg.value().decode('utf-8'))
            print(f"✅ Received message: {weather_data}")
            self.store_weather_data_in_db(weather_data)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ Error processing message: {e}")

    def store_weather_data_in_db(self, weather_data: dict):
        """Store the weather data into the PostgreSQL database."""
        try:
            location_data = weather_data['location']
            location_name = location_data['name']
            location_country = location_data['country']

            location = self.db.query(Location).filter_by(name=location_name, country=location_country).first()

            if not location:
                location = Location(name=location_name, country=location_country)
                self.db.add(location)
                self.db.commit()
                self.db.refresh(location)

            new_weather = Weather(
                location_id=location.location_id,
                observation_time=weather_data['observation_time'],
                temperature=weather_data['temperature'],
                weather_descriptions=weather_data['weather_descriptions'],
            )

            self.db.add(new_weather)
            self.db.commit()
            print(f"✅ Stored weather data for location {location_name}, {location_country}")

        except SQLAlchemyError as e:
            self.db.rollback()
            print(f"❌ Error storing data: {e}")
        except Exception as e:
            self.db.rollback()
            print(f"❌ Unexpected error: {e}")
