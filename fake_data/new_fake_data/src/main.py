"""Main module."""

import logging
import random
import sys
from time import sleep

from faker import Faker

from sqlalchemy import func
from sqlalchemy.orm import load_only, sessionmaker


import db
from auth_utils import generate_roles, generate_users
from auth_models import User, Role, LogHistory
from settings import settings


# log settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# faker settings
fake: Faker = Faker(['it_IT', 'en_US', 'de_DE', 'fr_FR'])


def wait_db(engine, tables: tuple, timeout_min: int = 2):
    timeout = timeout_min * 60
    while timeout:
        for table in tables:
            if not engine.dialect.has_table(engine, table):
                sleep(2)
                timeout -= 2
            else:
                return
    print(f'Engine: {engine}')
    print(f'Tables: {tables}')
    raise Exception('Timeout of waiting DB.')


def main():

    db.init_auth_db(settings.auth_db_url)
    auth_db = db.get_auth_db()

    db.init_movies_db(settings.movies_db_url)
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


if __name__ == '__main__':
    main()
