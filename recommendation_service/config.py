"""Config module for FastAPI project."""
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings

# load_dotenv здесь нужен несмотря на наличие pydantic,
# так как pydantic не умеет искать env в parent директориях
load_dotenv()
logger.level("DEBUG")


class Settings(BaseSettings):
    project_name: str = "recommendations_api"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    class Config:
        case_sensitive = False
        env_file = ".recom.env"
        env_file_encoding = "utf-8"


settings = Settings()
