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
        self, user_id: str
    ) -> list[WatchingHistory]:
        """Return user watching history."""
        collection = self.db[user_id]
        history = [d async for d in collection.find()]
        return history

    async def get_last_records_for_user(
        self, user_id: str, limit: int = 1000
    ) -> list[WatchingHistory]:
        """Return the latest watching history items."""
        collection = self.db[user_id]
        history = collection.find({}).sort([('$natural', -1)]).limit(limit)
        return [d async for d in history]

    async def add_history_record(self, user_id: str, film_id: str) -> None:
        """Add new watching history record."""
        collection = self.db[user_id]
        r = await collection.find({'film_id': film_id})
        if r:
            await collection.delete_one({'film_id': film_id})
        await collection.insert_one({'film_id': film_id})