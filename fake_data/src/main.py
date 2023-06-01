"""Main module."""

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

import db
import logger
from auth_db_utils import generate_roles, generate_users
from movies_db_utils import (
    generate_film_works, generate_genres, generate_persons
)
from settings import settings
from utils import wait_db
from watching_history_utils import generate_watching_history


@contextmanager
def sqlalchemy_session(engine):
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    yield session
    session.close()


def generate_first_data():
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

        generate_watching_history(auth_session, movies_session)


def main():

    logger.logger = logger.set_log_settings()

    db.init_auth_db(settings.auth_db_url)
    db.init_movies_db(settings.movies_db_url)

    generate_first_data()


if __name__ == '__main__':
    main()
