# FastAPI & Kafka Application

A simple weather data streaming demo using Kafka, PostgreSQL, and FastAPI.

##  Quick Start

```bash
# Clone and start
git clone https://github.com/wissemhammoudi/FastApiAndKafka.git
cd FastApiAndKafka
docker-compose up --build

# Access: http://localhost:8000
# Docs: http://localhost:8000/docs
```

##   What It Does

1. **Producer**: Generates weather data for 5 cities every 10 seconds
2. **Kafka**: Streams data through topics
3. **Consumer**: Stores data in PostgreSQL
4. **API**: Retrieves data for display

## 📁 Structure

```
├── app/                    # FastAPI app
├── docs/                   # Documentation
├── docker-compose.yml      # Docker setup
└── requirements.txt        # Dependencies
```

##  Documentation

- **[Complete Guide](./docs/README.md)** - Full documentation
- **[API Reference](./docs/api.md)** - API endpoints
- **[Services](./docs/)** - Individual service docs


