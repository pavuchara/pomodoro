import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", "random_key")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_LIFETIME = timedelta(minutes=30)


POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DRIVER: str = os.getenv("POSTGRES_DRIVER", "asyncpg")

DATABASE_URL = (
    f"postgresql+{POSTGRES_DRIVER}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
)


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
