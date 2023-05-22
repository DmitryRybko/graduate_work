"""Config module to save app settings."""

from pydantic import BaseSettings


class Config(BaseSettings):
    """Config."""

    title: str = 'Project title'
    port_to_run: str = '8014'

    mongo_db_url: str = ''
    debug: str = 'False'


config = Config()
