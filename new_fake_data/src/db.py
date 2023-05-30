"""Db module."""

import sqlalchemy as db

from settings import settings


auth_db = None
movies_db = None


def get_auth_db():
    """Return auth_db."""
    return auth_db


def get_movies_db():
    """Return movies_db."""
    return movies_db


def init_auth_db(url: str) -> None:
    global auth_db
    auth_db = db.create_engine(url)


def init_movies_db(url: str) -> None:
    global movies_db
    movies_db = db.create_engine(url)


init_auth_db(settings.auth_db_url)
