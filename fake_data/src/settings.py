#!/usr/bin/env python3
"""Settings module."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class for the app."""

    POSTGRES_HOST: str = 'movies_db'
    POSTGRES_PORT: str = '5432'
    POSTGRES_USER: str = 'app'
    POSTGRES_PASSWORD: str = '123qwe'
    POSTGRES_DB: str = 'movies_database'

    @property
    def movie_db_connect_data(self):
        return {
            'dbname': self.POSTGRES_DB,
            'host': self.POSTGRES_HOST,
            'port': self.POSTGRES_PORT,
            'user': self.POSTGRES_USER,
            'password': self.POSTGRES_PASSWORD
        }

    genre_table_name: str = 'genre'
    person_table_name: str = 'person'
    filmwork_table_name: str = 'film_work'
    genre_filmwork_table_name: str = 'genre_film_work'
    person_filmwork_table_name: str = 'person_film_work'

    genres_size: int = 100
    person_size: int = 5000
    filmwork_size: int = 1000

    batch_size: int = 1000

    debug: bool = True

    # Auth settings
    AUTH_POSTGRES_HOST: str = 'auth'
    AUTH_POSTGRES_PORT: str = '5432'
    AUTH_POSTGRES_USER: str = 'app'
    AUTH_POSTGRES_PASSWORD: str = '123qwe'
    AUTH_POSTGRES_DB: str = 'auth'

    auth_user_table_name: str = 'user'
    auth_role_table_name: str = 'role'
    auth_log_history_table_name: str = 'log_history'
    auth_user_role_table_name: str = 'user_role'

    @property
    def auth_db_connect_data(self):
        return {
            'dbname': self.AUTH_POSTGRES_DB,
            'host': self.AUTH_POSTGRES_HOST,
            'port': self.AUTH_POSTGRES_PORT,
            'user': self.AUTH_POSTGRES_USER,
            'password': self.AUTH_POSTGRES_PASSWORD
        }

    role_size: int = 10
    user_size: int = 100
    log_history_size: int = 100

    # watching history
    watching_history_size: int = 100

    mongo_db_url: str = ''
    mongo_db_db_name: str = 'db'
    mongo_db_collection_name: str = 'collection'


settings = Settings()
