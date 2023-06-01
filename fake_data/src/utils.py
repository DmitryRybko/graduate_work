"""Utils module."""

import random
import time
from time import sleep
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

import db
from auth_db_utils import generate_a_new_user, generate_roles, generate_users
from logger import get_logger
from movies_db_utils import (
    generate_a_new_film_work, generate_film_works,
    generate_genres, generate_new_person, generate_persons
)
from settings import settings
from watching_history_utils import (
    generate_watching_history, generate_new_watched_film
)

logger = get_logger()


@contextmanager
def sqlalchemy_session(engine):
    """Return session. It is context manager."""
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    yield session
    session.close()


async def generate_first_data():
    """Generate firs part of fake data to test."""
    auth_db = db.get_auth_db()
    movies_db = db.get_movies_db()

    # Wait auth_db
    wait_db(
        auth_db,
        (
            settings.user_table_name,
            settings.role_table_name,
            settings.log_history_table_name,
            settings.user_role_table_name
        )
    )

    wait_db(
        movies_db,
        (
            settings.person_table_name,
            settings.genre_table_name,
            settings.person_film_work_table_name,
            settings.genre_film_work_table_name,
            settings.film_work_table_name,
        ),
        settings.movies_schema_name
    )
    with (
        sqlalchemy_session(auth_db) as auth_session,
        sqlalchemy_session(movies_db) as movies_session
    ):

        generate_roles(auth_session)
        generate_users(auth_session)

        generate_genres(movies_session)
        generate_persons(movies_session)
        generate_film_works(movies_session)

        await generate_watching_history(auth_session, movies_session)


async def generate_data_by_the_time() -> None:
    """Generate one by one items in the project DB."""
    auth_db = db.get_auth_db()
    movies_db = db.get_movies_db()
    watching_history_db = db.get_watching_history_db()

    actions: tuple = ('film_work', 'person', 'user', 'watched_film')

    while True:
        with (
            sqlalchemy_session(auth_db) as auth_session,
            sqlalchemy_session(movies_db) as movies_session
        ):
            action = random.choice(actions)
            if action == 'film_work':
                logger
                generate_a_new_film_work(movies_session)
            elif action == 'person':
                generate_new_person(movies_session)
            elif action == 'user':
                generate_a_new_user(auth_session)
            elif action == 'watched_film':
                await generate_new_watched_film(
                    auth_session, movies_session, watching_history_db
                )
            time.sleep(random.randint(1, 5))


def wait_db(
    engine, tables: tuple, schema: str = 'public', timeout_min: int = 2
):
    """Wait when all db and all tables are available."""
    logger.debug(f'Engine: {engine}; Tables: {tables}; Timeout: {timeout_min}')
    timeout = timeout_min * 60
    for table in tables:
        while True:
            logger.debug(f'Table to wait {table}')
            if engine.dialect.has_table(engine, table, schema=schema):
                logger.debug(f'Table {table} is available')
                break
            sleep(2)
            timeout -= 2

            if timeout <= 0:
                raise Exception('Timeout of waiting DB.')
