# Location Service

## Overview
Retrieves location data from PostgreSQL database. Data is stored by the Kafka consumer service.

## API Endpoint

### Get Location Data
```http
GET /location/locations/
```

**Parameters**: `limit` (optional, default: 10)

**Example**:
```bash
curl -X GET "http://localhost:8000/location/locations/?limit=5"
```

## Data Structure

- **Location Table**: Stores city name and country
- **Weather Reference**: Links to weather table via location_id
- **Relationship**: One-to-many (Location → Weather)

## Debug

```bash
# Check location data
docker exec -it postgres psql -U admin -d weather_db -c "SELECT COUNT(*) FROM \"Location\";"

# Check location records
docker exec -it postgres psql -U admin -d weather_db -c "SELECT * FROM \"Location\" ORDER BY location_id DESC LIMIT 5;"
```

## Related Docs

- **[Complete Guide](./README.md)** - Project overview
- **[API Reference](./api.md)** - All endpoints
