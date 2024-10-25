import os
from dotenv import load_dotenv

load_dotenv()


POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test")
POSTGRES_USER: str = os.getenv("POSTGRES_USER", "test")
POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "test")
POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}"
)


REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
