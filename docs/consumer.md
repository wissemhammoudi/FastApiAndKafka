# Consumer Service

## Overview
Processes Kafka messages and stores weather data in PostgreSQL database.

## API Endpoint

### Start Consumer
```http
POST /consumer/start_consumer
```



## Data Flow

1. **Receive Message**: Gets weather data from Kafka topic
2. **Extract Location**: Creates/updates location record
3. **Store Weather**: Saves weather observation with location reference
4. **Commit Offset**: Marks message as processed


## Debug

```bash
# Check consumer logs
docker logs fastapi-kafka-app

# Monitor consumer group
docker exec -it kafka kafka-consumer-groups --bootstrap-server kafka:9092 --describe --group weather-consumer-group

# Check database records
docker exec -it postgres psql -U admin -d weather_db -c "SELECT COUNT(*) FROM \"Weather\";"
```

## Related Docs

- **[Complete Guide](./README.md)** - Project overview
- **[API Reference](./api.md)** - All endpoints
