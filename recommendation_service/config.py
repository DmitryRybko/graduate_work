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

    film_api_url: str = 'http://movies:8001'
    watching_history_api_url: str = 'http://watching_history:8014'

    @property
    def get_warching_history_url(self) -> str:
        return f'{self.watching_history_api_url}/get'

    @property
    def get_genres_url(self) -> str:
        return f'{self.film_api_url}/api/v1/films/get_genres'

    @property
    def get_recommendations_url(self) -> str:
        return f'{self.film_api_url}/api/v1/films/get_recommendations'

    class Config:
        case_sensitive = False
        env_file = ".recom.env"
        env_file_encoding = "utf-8"


settings = Settings()
