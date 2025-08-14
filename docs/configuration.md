# Configuration Guide

## Environment Setup

Create `.env` file in `app/core/` directory:

```env
# Database
DATABASE_NAME = "postgresql+psycopg2"
USERNAME = "admin"
PASSWORD = "admin"
HOST = "postgres"
DATABASE = "weather_db"
PORT = 5432

# Kafka
KAFKA_BROKER = "broker:9092"
```

## Docker Services

- **FastAPI App**: Port 8000
- **PostgreSQL**: Port 5432
- **Kafka**: Port 9092
- **Zookeeper**: Port 2181

## Quick Start

```bash
docker-compose up --build
```

For detailed setup, see [Complete Guide](./README.md).
