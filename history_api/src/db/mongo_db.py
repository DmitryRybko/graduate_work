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
        collection = self.db[self.collection_name]
        history = await collection.find({'user_id': user_id})
        return history

    async def get_last_1000_records_for_user(
        self, user_id: str
    ) -> list[WatchingHistory]:
        """Return the latest watching history items."""
        collection = self.db[self.collection_name]
        history = await collection.find(
            {'user_id': user_id}
        ).sort([('$natural', -1)]).limit(1000)
        return history
