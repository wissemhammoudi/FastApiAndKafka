# Kafka, PostgreSQL & FastAPI Application

This repository contains an application that integrates **Apache Kafka**, **PostgreSQL**, and **FastAPI**. The application includes endpoints for managing Kafka topics, starting/stopping producers and consumers, and retrieving weather and location data.

## Overview

The application consists of five main components:

1. **Kafka Topics Management**  
   - Create and list all Kafka topics.

2. **Kafka Producer Control**  
   - Start and stop a Kafka producer.

3. **Kafka Consumer Control**  
   - Start a Kafka consumer to process messages.

4. **Weather Data Retrieval**  
   - Retrieve weather data to verify the producer-consumer workflow.

5. **Location Data Retrieval**  
   - Retrieve location data to verify the producer-consumer workflow.

## Tech Stack

- **Apache Kafka** – Message streaming and topic management.
- **PostgreSQL** – Relational database for data persistence.
- **FastAPI** – High-performance REST API.
- **Docker** – Containerization for easy deployment.

## Getting Started

### Prerequisites

- **Docker Desktop**should be installed.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/wissemhammoudi/FastApiAndKafka.git
   cd FastApiAndKafka
   ```

2. **Configure Environment Variables:**

   Create a `.env` file in the root directory (or core directory if applicable) with the following content:

   ```dotenv
   DATABASE_NAME = "postgresql+psycopg2"
   USERNAME = "admin"
   PASSWORD = "admin"
   HOST = "postgres"
   DATABASE = "weather_db"
   PORT = 5432
   KAFKA_BROKER = "broker:9092"
   ```

3. **Run the Project with Docker:**

   Ensure you have **Docker Desktop** opened Then run:

   ```bash
   docker-compose up --build
   ```

## API Endpoints

### Kafka Topics

- **POST `/topic/create_topic/`**: Create a Kafka Topic  
  Creates a Kafka topic dynamically with user-defined partitions, replication factor, and retention policies.
  - **Parameters**:
    - `topic_name` (string, required): The name of the topic.
    - `num_partitions` (integer, optional, default: 1): The number of partitions for the topic.
    - `replication_factor` (integer, optional, default: 1): The replication factor for the topic.
    - `retention_ms` (integer, optional): The retention time in milliseconds.
    - `retention_bytes` (integer, optional): The retention size in bytes.


- **GET `/topic/topics/`**: List all Kafka Topics  
  Fetches all Kafka topics available in the broker.
  - **Parameters**: None.



### Kafka Producer

- **POST `/producer/start_producer/`**: Start Kafka Producer  
  Starts the Kafka weather data producer.
  - **Parameters**:
    - `kafka_topic` (string, required): The Kafka topic to produce data to.



- **POST `/producer/stop_producer/`**: Stop Kafka Producer  
  Stops the Kafka weather data producer.
  - **Parameters**: None.

### Kafka Consumer

- **POST `/consumer/start_consumer/`**: Start Kafka Consumer  
  Starts the Kafka consumer thread.
  - **Parameters**:
    - `kafka_topic` (string, required): The Kafka topic to consume data from.


### Locations

- **GET `/location/locations/`**: Read Locations  
  Fetches location data from the database with an optional limit.
  - **Parameters**:
    - `limit` (integer, optional, default: 10): Limit the number of locations to fetch.


### Weather

- **GET `/Weather/weathers/`**: Read Weather Data  
  Fetches weather data from the database with an optional limit.
  - **Parameters**:
    - `limit` (integer, optional, default: 10): Limit the number of weather records to fetch.

## Usage Example

After starting the application, you can interact with the API using tools like **curl**, **Postman**, or via the **Swagger UI** at [http://localhost:8000/docs](http://localhost:8000/docs).

For example, to retrieve weather data with a limit of 5 records:

```bash
curl -X GET "http://localhost:8000/weather/weathers/?limit=5" -H "accept: application/json"
```

## Project Structure

```
├── app
│   ├── main.py                 # Application entry point
│   ├── routers                 # API route definitions
│   │   ├── topic.py            # Kafka topic related routes
│   │   ├── producer.py         # Kafka producer related routes
│   │   ├── consumer.py         # Kafka consumer related routes
│   │   ├── weather.py          # Weather data related routes
│   │   └── location.py         # Location data related routes
│   ├── services                # Business logic for Kafka and data handling
│   │   ├── topic.py            # Kafka topic related logic
│   │   ├── producer.py         # Kafka producer related logic
│   │   ├── consumer.py         # Kafka consumer related logic
│   │   ├── weather.py          # Weather data related logic
│   │   └── location.py         # Location data related logic
│   ├── models                  # SQLAlchemy models
│   │   ├── base.py             # Base class for models
│   │   └── model.py            # Actual models for the app
│   ├── schemas                 # Pydantic schemas
│   │   ├── weather.py          # Weather data validation
│   │   └── location.py         # Location data validation
│   ├── dependencies            # Dependency injection modules
│   │   └── database.py         # Database connection and session
│   ├── core                    # Core configuration files
│   │   ├── __init__.py         # Initialize core package
│   │   ├── database.py         # Database helper functions
│   │   ├── config.py           # Configuration for the app
│   │   └── .env                # Environment variables
│
├── requirements.txt            # Project dependencies
├── docker-compose.yml          # Docker Compose configuration
└── README.md                   # Project documentation (e.g., API usage, setup)

```

