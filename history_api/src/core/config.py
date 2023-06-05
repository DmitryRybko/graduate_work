from loguru import logger
from pydantic import BaseSettings, Field

logger.level("DEBUG")

class Config(BaseSettings):
    """Base config."""

    title: str = 'Project title'
    port_to_run: str = '8014'

    mongo_db_url: str = ''
    mongo_db_db_name: str = 'db'
    mongo_db_collection_name: str = 'email2@emails.ru'


class LocalConfig(Config):
    """Local config."""

    mongo_db_url: str = Field(default='localhost:27017', env='MONGO_DB_URL_LOCAL')


class DockerConfig(Config):
    """Docker config."""

    mongo_db_url: str = Field(default='watching_history_db', env='MONGO_DB_URL_DOCKER')


def get_config(mode: str) -> Config:
    """Get config based on mode."""
    if mode == 'local':
        logger.info("local mode")
        return LocalConfig()
    elif mode == 'docker':
        logger.info("docker mode")
        return DockerConfig()
    else:
        raise ValueError(f'Invalid mode: {mode}')


# mode = 'local'
mode = 'docker'

config = get_config(mode)
