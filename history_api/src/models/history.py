"""Watching history models."""

from uuid import UUID

from pydantic import BaseModel


class WatchingHistory(BaseModel):
    """Watching History model."""

    film_id: str
