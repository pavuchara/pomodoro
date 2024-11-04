import os

from dotenv import load_dotenv

load_dotenv()

RABBITMQ_DEFAULT_USER: str = os.getenv("RABBITMQ_DEFAULT_USER", "guest")
RABBITMQ_DEFAULT_PASS: str = os.getenv("RABBITMQ_DEFAULT_PASS", "guest")
AMQP_HOST: str = os.getenv("AMQP_HOST", "localhost")
AMQP_PORT: str = os.getenv("AMQP_PORT", "5672")
AMQP_URL: str = f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{AMQP_HOST}:{AMQP_PORT}//"

SMTP_HOST: str = os.getenv("SMTP_HOST", "")
SMTP_PORT: int = int(os.getenv("SMTP_PORT") or 6379)
EMAIL_FROM: str = os.getenv("EMAIL_FROM", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
