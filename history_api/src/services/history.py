"""Services history module."""

from functools import lru_cache

from fastapi import Depends

from db.base_db import BaseDB
from db.db import get_db


class WatchingHistoryService:
    """Notification service."""

    def __init__(self, db: BaseDB) -> None:
        """Init WatchingHistoryService."""
        self.db: BaseDB = db

    async def get_history_by_user_id(self, user_id: str):
        """Return all user history."""
        history = await self.db.get_history_for_user(user_id)
        return history

    async def get_latest_user_history(self, user_id: str):
        """Return the latest user history items."""
        history = await self.db.get_latest_user_history(user_id)
        return history


@lru_cache()
def get_watching_history_service(
    db: BaseDB = Depends(get_db)
) -> WatchingHistoryService:
    """Return WatchingHistoryService item."""
    return WatchingHistoryService(db)
