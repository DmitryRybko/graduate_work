"""Services history module."""

from functools import lru_cache

from fastapi import Depends

from db.base_db import BaseDB
from db.db import get_db
from models.history import WatchingHistory


class WatchingHistoryService:
    """Notification service."""

    def __init__(self, db: BaseDB) -> None:
        """Init WatchingHistoryService."""
        self.db: BaseDB = db

    async def get_history_by_user_id(
        self, user_id: str, limit: int = 1000
    ) -> list[WatchingHistory]:
        """Return all user history."""
        history: list[WatchingHistory] = await self.db.get_history_for_user(
            user_id, limit
        )
        return history

    async def add_watched_film(self, user_id: str, film_id: str) -> str | None:
        """Add new item in watching history."""
        watched_film: WatchingHistory = WatchingHistory(
            user_id=user_id, film_id=film_id
        )
        try:
            await self.db.add_history_record(
                watched_film.user_id, watched_film.film_id
            )
        except Exception as e:
            return str(e)
        return None

    async def is_watched(self, user_id: str, film_id: str) -> bool | str:
        """Return True if the user has watched the film."""
        try:
            return self.db.film_is_watched(user_id, film_id)
        except Exception as e:
            return str(e)


@lru_cache()
def get_watching_history_service(
    db: BaseDB = Depends(get_db)
) -> WatchingHistoryService:
    """Return WatchingHistoryService item."""
    return WatchingHistoryService(db)
