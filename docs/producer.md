# Producer Service

## Overview
Generates weather data and publishes it to Kafka topics using confluent-kafka library.

## API Endpoints

### Start Producer
```http
POST /producer/start_producer
```

**Parameters**: `kafka_topic` (required)

**Example**:
```bash
curl -X POST "http://localhost:8000/producer/start_producer?kafka_topic=weather-data"
```

### Stop Producer
```http
POST /producer/stop_producer
```

## Data Generation

### Cities
- New York, London, Paris, Berlin, Tokyo

### Weather Data
```json
{
  "observation_time": "14:30:00",
  "temperature": 25,
  "weather_descriptions": "Sunny",
  "location": {"name": "New York", "country": "USA"}
}
```

### Settings
- **Update Interval**: Every 10 seconds
- **Temperature Range**: -10°C to 35°C
- **Weather Types**: Sunny, Cloudy, Rainy, Snowy, Foggy, Windy

## Data Flow

1. **City Selection**: Randomly picks a city from the list
2. **Weather Generation**: Creates random temperature and weather description
3. **Data Assembly**: Combines city, weather, and timestamp
4. **Message Publishing**: Sends to Kafka topic every 10 seconds

## Sending Modes

- **Fire-and-forget**: `producer.produce()` without flush
- **Synchronous**: `producer.produce()` + `producer.flush()`
- **Asynchronous**: `producer.produce()` with callback

## Debug

```bash
# Check producer logs
docker logs fastapi-kafka-app

# Monitor Kafka topics
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic weather-data --from-beginning
```

## Related Docs

- **[Complete Guide](./README.md)** - Project overview
- **[API Reference](./api.md)** - All endpoints
