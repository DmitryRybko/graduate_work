"""Watching history utils module."""

import logging

from motor.motor_asyncio import AsyncIOMotorClient

from auth_db_utils import get_all_users
from movies_db_utils import get_random_film_works

from settings import settings


def generate_watching_history(auth_session, movies_session) -> None:
    """Generate watching history for all users."""
    client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongo_db_url)
    db = client[settings.mongo_db_db_name]
    collection = db[settings.mongo_db_collection_name]

    film_list: list[dict] = []

    users = get_all_users(auth_session)
    for user in users:
        film_works: list = get_random_film_works(movies_session)
        for film_work in film_works:
            logging.info(f'User id: {user.id}; Film id: {film_work.id}')
            film_list.append({'film_id': film_work.id, 'user_id': user.id})
            if len(film_list) >= settings.batch_size:
                collection.insert_many(film_list)
                film_list = []
    if film_list:
        collection.insert_many(film_list)
