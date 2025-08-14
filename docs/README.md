# FastAPI & Kafka Application - Complete Guide

## Overview

Simple weather data streaming demo using Kafka, PostgreSQL, and FastAPI. Generates weather data for 5 cities every 10 seconds.

## 🏗️ Architecture

```
FastAPI → Kafka Producer → Kafka Topics → Kafka Consumer → PostgreSQL
```

## 🛠️ Tech Stack

- **FastAPI** – REST API
- **Apache Kafka** – Message streaming (confluent-kafka)
- **PostgreSQL** – Database
- **Docker** – Containerization

## 🚀 Setup

1. **Clone & Start**
   ```bash
   git clone https://github.com/wissemhammoudi/FastApiAndKafka.git
   cd FastApiAndKafka
   docker-compose up --build
   ```

2. **Environment**
   Create `.env` file in `app/core/`:
   ```dotenv
   DATABASE_NAME = "postgresql+psycopg2"
   USERNAME = "admin"
   PASSWORD = "admin"
   HOST = "postgres"
   DATABASE = "weather_db"
   PORT = 5432
   KAFKA_BROKER = "broker:9092"
   ```

3. **Access**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs

## 📊 Data

### Weather Data
```json
{
  "observation_time": "14:30:00",
  "temperature": 25,
  "weather_descriptions": "Sunny",
  "location": {"name": "New York", "country": "USA"}
}
```

### Cities
- New York, London, Paris, Berlin, Tokyo
- Weather: Sunny, Cloudy, Rainy, Snowy, Foggy, Windy
- Temperature: -10°C to 35°C

## 🔄 Workflow

1. **Create Topic**
   ```bash
   curl -X POST "http://localhost:8000/topic/create_topic?topic_name=weather-data"
   ```

2. **Start Producer**
   ```bash
   curl -X POST "http://localhost:8000/producer/start_producer?kafka_topic=weather-data"
   ```

3. **Start Consumer**
   ```bash
   curl -X POST "http://localhost:8000/consumer/start_consumer?kafka_topic=weather-data"
   ```

4. **Check Data**
   ```bash
   curl -X GET "http://localhost:8000/Weather/weathers/?limit=5"
   curl -X GET "http://localhost:8000/location/locations/?limit=5"
   ```

## 📡 API Endpoints

- `POST /topic/create_topic` - Create topics
- `GET /topic/topics` - List topics
- `POST /producer/start_producer` - Start producer
- `POST /producer/stop_producer` - Stop producer
- `POST /consumer/start_consumer` - Start consumer
- `GET /Weather/weathers/` - Get weather data
- `GET /location/locations/` - Get location data

## 🐳 Docker Services

- FastAPI App
- PostgreSQL
- Kafka
- Zookeeper

## 🚨 Troubleshooting

### Common Issues
- **Producer not starting**: Check Kafka connectivity
- **Consumer not processing**: Verify topic exists
- **No data**: Ensure consumer is running

### Debug
```bash
# Check logs
docker logs fastapi-kafka-app

# Monitor Kafka
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic weather-data --from-beginning

# Check database
docker exec -it postgres psql -U admin -d weather_db -c "SELECT COUNT(*) FROM \"Weather\";"
```

## 📚 More Docs

- **[API Reference](./api.md)** - Complete API docs
- **[Services](./)** - Individual service guides
