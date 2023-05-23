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

    AUTH_POSTGRES_HOST: str = 'auth'
    AUTH_POSTGRES_PORT: str = '5432'
    AUTH_POSTGRES_USER: str = 'app'
    AUTH_POSTGRES_PASSWORD: str = '123qwe'
    AUTH_POSTGRES_DB: str = 'auth'

    auth_user_table_name: str = 'user'
    auth_role_table_name: str = 'role'
    auth_log_history_table_name: str = 'log_history'

    @classmethod
    def auth_db_connect_data(self):
        return {
            'POSTGRES_DB': self.jAUTH_POSTGRES_DB,
            'POSTGRES_HOST': self.AUTH_POSTGRES_HOST,
            'POSTGRES_PORT': self.AUTH_POSTGRES_PORT,
            'POSTGRES_USER': self.AUTH_POSTGRES_USER,
            'POSTGRES_PASSWORD': self.AUTH_POSTGRES_PASSWORD
        }


settings = Settings()
