"""Main module."""

import asyncio

import db
import logger

from settings import settings
from utils import generate_first_data, generate_data_by_the_time


async def main():

    logger.logger = logger.set_log_settings()

    db.init_auth_db(settings.auth_db_url)
    db.init_movies_db(settings.movies_db_url)
    db.init_watching_history_db(
        settings.mongo_db_url, settings.mongo_db_db_name
    )

    await generate_first_data()
    await generate_data_by_the_time()


if __name__ == '__main__':
    asyncio.run(main())
