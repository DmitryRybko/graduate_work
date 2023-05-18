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
    person_size: int = 500000
    filmwork_size: int = 100000

    batch_size: int = 1000

    debug: bool = True


settings = Settings()
