"""Module to work with mongoDB."""

from logging import getLogger

from motor.motor_asyncio import AsyncIOMotorClient

from db import base_db
from models.history import WatchingHistory


logger = getLogger(__name__)


class MondoDB(base_db.BaseDB):
    """Class to work with Mongo as DB instance."""

    def __init__(self, db_url: str, db_name: str, collection_name):
        """Init MongoDB class."""
        self.db_url: str = db_url
        self.db_name: str = db_name
        self.collection_name: str = collection_name
        self.client: AsyncIOMotorClient = AsyncIOMotorClient(self.db_url)
        self.db = self.client[self.db_name]

    async def get_history_for_user(
        self, user_id: str, limit: int = 1000
    ) -> list[WatchingHistory]:
        """Return user watching history."""
        collection = self.db[self.collection_name]
        history: list[WatchingHistory] = collection.find(
            {'user_id': user_id}).sort([('$natural', -1)]).limit(limit)
        logger.info('loading history')
        return [d async for d in history]

    async def add_history_record(self, user_id: str, film_id: str) -> None:
        """Add new watching history record."""
        collection = self.db[self.collection_name]
        r = await collection.find_one({'film_id': film_id, 'user_id': user_id})
        if r:
            await collection.delete_one(
                {'film_id': film_id, 'user_id': user_id}
            )
        await collection.insert_one({'film_id': film_id, 'user_id': user_id})

    async def film_is_watched(self, user_id: str, film_id: str) -> bool:
        """Return True if the user has wathed the film."""
        collection = self.db[self.collection_name]
        r = await collection.find({'film_id': film_id, 'user_id': user_id})
        return True if r else False
