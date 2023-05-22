"""Watching history models."""

from uuid import UUID, uuid4

from pydantic import BaseModel


class WatchingHistory(BaseModel):
    """Watching History model."""

    id: UUID = uuid4()
    user_id: UUID
    film_id: UUID
