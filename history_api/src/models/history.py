"""Watching history models."""

from pydantic import BaseModel


class WatchingHistory(BaseModel):
    """Watching History model."""

    user_id: str
    film_id: str
