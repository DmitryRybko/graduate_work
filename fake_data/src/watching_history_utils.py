"""Watching history utils module."""

import logging


from auth_db_utils import get_all_users, get_random_user
from movies_db_utils import get_random_film_works

from logger import get_logger
from settings import settings

log = get_logger()


async def generate_watching_history(
    auth_session,
    movies_session,
    watching_history_db
) -> None:
    """Generate watching history for all users."""
    collection = watching_history_db[settings.mongo_db_collection_name]

    film_list: list[dict] = []

    users = get_all_users(auth_session)
    for user in users:
        film_works: list = get_random_film_works(movies_session)
        for film_work in film_works:
            logging.info(f'User id: {user.id}; Film id: {film_work.id}')
            film_list.append({'film_id': film_work.id, 'user_id': user.id})
            if len(film_list) >= settings.batch_size:
                await collection.insert_many(film_list)
                film_list = []
    if film_list:
        collection.insert_many(film_list)


async def generate_new_watched_film(
    auth_session, movies_session, watching_history_db
) -> None:
    """Generate new record in watching history."""
    user = get_random_user(auth_session)
    film = get_random_film_works(movies_session, 1)[0]
    collection = watching_history_db[settings.mongo_db_collection_name]
    doc: dict = {'film_id': film.id, 'user_id': user.id}
    log.debug(doc)
    await collection.insert_one(doc)
