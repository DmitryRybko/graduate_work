"""Settings module."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """App settings."""

    # Auth
    auth_db_url: str = 'postgresql://user:password@auth_db:5432/auth'
    user_table_name: str = 'user'
    role_table_name: str = 'role'
    log_history_table_name: str = 'log_history'
    user_role_table_name: str = 'user_role'

    user_size: int = 100
    role_size: int = 50
    log_history_size: int = 100
    user_role_size: int = 5

    # Movies
    movies_db_url: str = 'postgres://app:123qwe@movies_db:5432/movies_db'
    movies_schema_name: str = 'content'
    filmwork_table_name: str = 'film_work'
    genre_table_name: str = 'genre'
    person_table_name: str = 'person'
    genre_film_work_table_name: str = 'genre_film_work'
    person_film_work_table_name: str = 'person_film_work'

    film_work_size: int = 100
    person_size: int = 500
    genre_size: int = 100
    person_film_work_size: int = 10
    genre_film_work_size: int = 3

    # Watching_history
    mondo_db_url: str = 'watching_history_db'
    mondog_db_db_name: str = 'watching_history'
    mongo_db_collection_name: str = 'user_history'

    watching_history_size: int = 100

    ###
    batch_size: int = 1000


settings: Settings = Settings()
