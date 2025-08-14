# Weather Service

## Overview
Retrieves weather data from PostgreSQL database. Data is stored by the Kafka consumer service.

## API Endpoint

### Get Weather Data
```http
GET /Weather/weathers/
```

**Parameters**: `limit` (optional, default: 10)

**Example**:
```bash
curl -X GET "http://localhost:8000/Weather/weathers/?limit=5"
```

## Data Structure

- **Weather Table**: Stores temperature, description, observation time
- **Location Reference**: Links to location table via location_id
- **Relationship**: One-to-many (Location → Weather)

## Debug

```bash
# Check weather data
docker exec -it postgres psql -U admin -d weather_db -c "SELECT COUNT(*) FROM \"Weather\";"

# Check latest records
docker exec -it postgres psql -U admin -d weather_db -c "SELECT * FROM \"Weather\" ORDER BY weather_id DESC LIMIT 5;"
```

## Related Docs

- **[Complete Guide](./README.md)** - Project overview
- **[API Reference](./api.md)** - All endpoints
