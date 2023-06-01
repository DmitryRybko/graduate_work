"""Config module for FastAPI project."""
from pydantic import BaseSettings


class Settings(BaseSettings):
    project_name: str = "recommendations_api"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    movies_api_url: str = "http://localhost:8001"
    watching_history_api_url: str = "http://localhost:8014"

    @property
    def get_genres_url(self):
        return f"{self.movies_api_url}/api/v1/films/get_genres"

    @property
    def get_watching_history_url(self):
        return f"{self.watching_history_api_url}/api/v1/history/get"

    @property
    def get_recommendations_url(self):
        return f"{self.movies_api_url}/api/v1/films/get_recommendations"
    
    log_level: str = "DEBUG"

    class Config:
        case_sensitive = False
        env_file = ".recom.env"
        env_file_encoding = "utf-8"
        dotenv_path = "../.recom.env"


settings = Settings()

