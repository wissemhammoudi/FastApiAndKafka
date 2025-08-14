# Kafka Service

## Overview
Manages Kafka topic creation and listing for the streaming platform.

## API Endpoints

### Create Topic
```http
POST /topic/create_topic
```

**Parameters**: `topic_name` (required), `num_partitions`, `replication_factor`

**Example**:
```bash
curl -X POST "http://localhost:8000/topic/create_topic?topic_name=weather-data&num_partitions=1"
```

### List Topics
```http
GET /topic/topics
```

**Response**: List of all available topics

## Topic Configuration

- **Partitions**: Distribute data across multiple partitions
- **Replication**: Ensure data durability through broker copies
- **Retention**: Configurable data retention policies

## Data Flow

1. **Topic Creation**: Create topics with custom configuration
2. **Message Storage**: Messages stored in partitions
3. **Data Distribution**: Parallel processing across partitions
4. **Consumer Access**: Multiple consumers can read from partitions

## Debug

```bash
# List topics
docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --list

# Describe topic
docker exec -it kafka kafka-topics --bootstrap-server kafka:9092 --describe --topic weather-data

# Monitor messages
docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic weather-data --from-beginning
```

## Related Docs

- **[Complete Guide](./README.md)** - Project overview
- **[API Reference](./api.md)** - All endpoints
