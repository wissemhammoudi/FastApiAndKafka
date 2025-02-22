# Kafka, PostgreSQL & FastAPI Application

This repository contains an application that integrates **Apache Kafka**, **PostgreSQL**, and **FastAPI** to provide a real-time messaging and data management solution. The application includes endpoints for managing Kafka topics, starting/stopping producers and consumers, and retrieving weather and location data.

## Overview

The application consists of five main components:

1. **Kafka Topics Management**  
   Create and list all Kafka topics.

2. **Kafka Producer Control**  
   Start and stop a Kafka producer.

3. **Kafka Consumer Control**  
   Start a Kafka consumer to process messages.

4. **Weather Data Retrieval**  
   Retrieve weather data stored in PostgreSQL.

5. **Location Data Retrieval**  
   Retrieve location data to verify the producer-consumer workflow.

## Features

- **Topic Management:** Create and list Kafka topics.
- **Producer Management:** Easily start and stop your Kafka producer.
- **Consumer Management:** Launch a Kafka consumer for real-time processing.
- **Weather Data:** Fetch weather information from your PostgreSQL database.
- **Location Data:** Retrieve location details to ensure data flow is working as expected.

## Tech Stack

- **Apache Kafka** – Message streaming and topic management.
- **PostgreSQL** – Relational database for data persistence.
- **FastAPI** – High-performance REST API.
- **Docker (Optional)** – Containerization for easy deployment.

## Getting Started

### Prerequisites

- Python 3.8+
- Kafka instance (or Dockerized Kafka)
- PostgreSQL database
- (Optional) Docker & Docker Compose

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
Create a Virtual Environment & Install Dependencies:

bash
Copier
Modifier
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure Environment Variables:

Create a .env file in the root directory with contents similar to:

dotenv
Copier
Modifier
KAFKA_BROKER=your_kafka_broker_address
DATABASE_URL=postgresql://username:password@localhost:5432/your_database
Run Database Migrations:

If using Alembic, run:

bash
Copier
Modifier
alembic upgrade head
Start the Application:

bash
Copier
Modifier
uvicorn main:app --reload
Docker Setup
If you prefer using Docker, ensure you have a proper docker-compose.yml file. Then run:

bash
Copier
Modifier
docker-compose up --build
API Endpoints
Kafka Topics
GET /topics/: List all Kafka topics.
POST /topics/: Create a new Kafka topic.
Kafka Producer
POST /producer/start/: Start the Kafka producer.
POST /producer/stop/: Stop the Kafka producer.
Kafka Consumer
POST /consumer/start/: Start the Kafka consumer.
Weather Data
GET /weather/weathers/: Retrieve weather data.
Query Parameter: limit (default: 10)
Location Data
GET /location/: Retrieve location data.
Usage Example
After starting the application, you can interact with the API using tools like curl, Postman, or via the Swagger UI at http://localhost:8000/docs.

For example, to retrieve weather data with a limit of 5 records:

bash
Copier
Modifier
curl -X GET "http://localhost:8000/weather/weathers/?limit=5" -H "accept: application/json"
Project Structure
bash
Copier
Modifier
├── app
│   ├── main.py                   # Application entry point
│   ├── routers                   # API route definitions
│   │   ├── topic.py
│   │   ├── producer.py
│   │   ├── consumer.py
│   │   ├── weather.py
│   │   └── location.py
│   ├── services                  # Business logic for Kafka and data handling
│   │   ├── consumer.py
│   │   ├── producer.py
│   │   └── weather.py
│   ├── models                    # SQLAlchemy models
│   │   └── model.py
│   ├── schemas                   # Pydantic schemas
│   │   └── weather.py
│   └── dependencies              # Dependency injection modules
│       └── database.py
├── requirements.txt
├── .env                        # Environment variables
└── docker-compose.yml          # Docker Compose configuration
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes.
Open a pull request.
License
This project is licensed under the MIT License.