from pydantic import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str = "mongodb://mongo:27017"
    MONGODB_DB: str = "testdb"

    class Config:
        env_file = ".env"

settings = Settings()
