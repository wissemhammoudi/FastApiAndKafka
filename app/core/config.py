from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database connection details
    DATABASE_NAME: str
    USERNAME: str
    PASSWORD: str
    HOST: str
    DATABASE: str
    PORT: int
    KAFKA_BROKER: str

    class Config:
        # Specify the path to your .env file
        env_file = "./core/.env"
