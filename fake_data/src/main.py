"""Main module."""

from sqlalchemy.orm import sessionmaker

import db
from auth_db_utils import generate_roles, generate_users
from movies_db_utils import (
    generate_film_works, generate_genres, generate_persons
)
from settings import settings
from utils import set_log_level, wait_db
from watching_history_utils import generate_watching_history


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

    AuthSession = sessionmaker(bind=auth_db, autoflush=False)
    auth_session = AuthSession()

    generate_roles(auth_session)
    generate_users(auth_session)

    MoviesSession = sessionmaker(bind=movies_db, autoflush=False)
    movies_session = MoviesSession()

    generate_genres(movies_session)
    generate_persons(movies_session)
    generate_film_works(movies_session)

    generate_watching_history(auth_session, movies_session)

    auth_session.close()
    movies_session.close()


def main():

    set_log_level()

    db.init_auth_db(settings.auth_db_url)
    db.init_movies_db(settings.movies_db_url)

    generate_first_data()


if __name__ == '__main__':
    main()
