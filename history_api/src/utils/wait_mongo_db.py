#!/usr/bin/env python3

from time import sleep

from motor.motor_asyncio import AsyncIOMotorClient

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Settings class."""

    mongo_db_url: str = ''
    mongo_db_db_name: str = 'db'
    mongo_db_collection_name: str = 'collection'


def main() -> None:
    """Wait when the Mongo DB is available to work."""
    timeout_min: int = 2
    timeout: int = timeout_min * 60
    settings: Settings = Settings()
    collection = None
    while collection is not None:
        try:
            client: AsyncIOMotorClient = AsyncIOMotorClient(
                settings.mongo_db_url
            )
            db = client[settings.mongo_db_db_name]
            collection = db[settings.mongo_db_collection_name]
        except Exception:
            timeout -= 1
            sleep(1)
            if timeout < 0:
                raise Exception(
                    (
                        'Timeout of waiting MongoDB. '
                        f'URL: {settings.mongo_db_url} '
                        f'DB name: {settings.mongo_db_db_name} '
                        f'Collection name: {settings.mongo_db_collection_name}'
                    )
                )


if __name__ == '__main__':
    main()
