# API Reference

## Base URL
```
http://localhost:8000
```

## Endpoints

### Create Kafka Topic
```http
POST /topic/create_topic
```

**Description**: Creates a Kafka topic dynamically with user-defined partitions, replication factor, and retention policies.

**Query Parameters**:
- `topic_name` (string, required): The name of the topic
- `num_partitions` (integer, optional, default: 1): Number of partitions
- `replication_factor` (integer, optional, default: 1): Replication factor
- `retention_ms` (integer, optional): Retention time in milliseconds
- `retention_bytes` (integer, optional): Retention size in bytes

**Response**:
- `200`: Topic created successfully
- `500`: Server error

**Example Request**:
```bash
curl -X POST "http://localhost:8000/topic/create_topic?topic_name=weather-data&num_partitions=3&replication_factor=1"
```

### List Topics
```http
GET /topic/topics
```

**Description**: Fetches all Kafka topics available in the broker.

**Response**:
- `200`: Topics list retrieved successfully
- `500`: Server error

**Example Response**:
```json
{
  "topics": [
    "weather-data",
    "location-data",
    "system-topic"
  ]
}
```

## Kafka Producer Endpoints

### Start Producer
```http
POST /producer/start_producer
```

**Description**: Starts the Kafka weather data producer.

**Query Parameters**:
- `kafka_topic` (string, required): The Kafka topic to produce data to

**Response**:
- `200`: Producer started successfully
- `500`: Server error

**Example Request**:
```bash
curl -X POST "http://localhost:8000/producer/start_producer?kafka_topic=weather-data"
```

**Example Response**:
```json
{
  "message": "Started producing weather updates for Kafka topic: weather-data"
}
```

### Stop Producer
```http
POST /producer/stop_producer
```

**Description**: Stops the Kafka weather data producer.

**Response**:
- `200`: Producer stopped successfully
- `500`: Server error

**Example Response**:
```json
{
  "message": "Weather producer stopped successfully"
}
```

## Kafka Consumer Endpoints

### Start Consumer
```http
POST /consumer/start_consumer
```

**Description**: Starts the Kafka consumer thread.

**Query Parameters**:
- `kafka_topic` (string, required): The Kafka topic to consume data from

**Response**:
- `200`: Consumer started successfully
- `500`: Server error

**Example Request**:
```bash
curl -X POST "http://localhost:8000/consumer/start_consumer?kafka_topic=weather-data"
```

## Weather Data Endpoints

### Get Weather Data
```http
GET /Weather/weathers/
```

**Description**: Fetches weather data from the database with an optional limit.

**Query Parameters**:
- `limit` (integer, optional, default: 10): Limit the number of weather records to fetch

**Response**:
- `200`: Weather data retrieved successfully
- `500`: Failed to fetch weather data

**Example Response**:
```json
[
  {
    "weather_id": 1,
    "location_id": 1,
    "observation_time": "14:30:00",
    "temperature": 25,
    "weather_descriptions": "Sunny"
  },
  {
    "weather_id": 2,
    "location_id": 2,
    "observation_time": "14:35:00",
    "temperature": 22,
    "weather_descriptions": "Cloudy"
  }
]
```

## Location Data Endpoints

### Get Location Data
```http
GET /location/locations/
```

**Description**: Fetches location data from the database with an optional limit.

**Query Parameters**:
- `limit` (integer, optional, default: 10): Limit the number of locations to fetch

**Response**:
- `200`: Location data retrieved successfully
- `500`: Failed to fetch location data

**Example Response**:
```json
[
  {
    "location_id": 1,
    "name": "New York",
    "country": "USA"
  },
  {
    "location_id": 2,
    "name": "London",
    "country": "UK"
  }
]
```

## Data Models

### Weather Data Structure
The producer generates weather data with the following structure:
```json
{
  "observation_time": "14:30:00",
  "temperature": 25,
  "weather_descriptions": "Sunny",
  "location": {
    "name": "New York",
    "country": "USA"
  }
}
```



## Usage Examples

### Complete Workflow
1. **Create a topic**:
   ```bash
   curl -X POST "http://localhost:8000/topic/create_topic?topic_name=weather-data&num_partitions=1"
   ```

2. **Start the producer**:
   ```bash
   curl -X POST "http://localhost:8000/producer/start_producer?kafka_topic=weather-data"
   ```

3. **Start the consumer**:
   ```bash
   curl -X POST "http://localhost:8000/consumer/start_consumer?kafka_topic=weather-data"
   ```

4. **Check weather data**:
   ```bash
   curl -X GET "http://localhost:8000/Weather/weathers/?limit=5"
   ```

5. **Check location data**:
   ```bash
   curl -X GET "http://localhost:8000/location/locations/?limit=5"
   ```

6. **Stop the producer**:
   ```bash
   curl -X POST "http://localhost:8000/producer/stop_producer"
   ```
-