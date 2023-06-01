"""Watching history models module."""

from pydantic import BaseModel


class WatchingHistory(BaseModel):
    film_id: str
