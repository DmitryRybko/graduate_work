"""Db module."""

from motor.motor_asyncio import AsyncIOMotorClient

import sqlalchemy as db


auth_db = None
movies_db = None

watching_history_db = None


def get_auth_db():
    """Return auth_db."""
    return auth_db


def get_movies_db():
    """Return movies_db."""
    return movies_db


def get_watching_history_db():
    """Return watching history DB."""
    return watching_history_db


def init_auth_db(url: str) -> None:
    """Init connect to auth db."""
    global auth_db
    auth_db = db.create_engine(url)


def init_movies_db(url: str) -> None:
    """Init connect to movies db."""
    global movies_db
    movies_db = db.create_engine(url)


def init_watching_history_db(url: str, db_name: str) -> None:
    """Init connect to watching history db."""
    global watching_history_db
    watching_history_db = AsyncIOMotorClient(url)[db_name]
