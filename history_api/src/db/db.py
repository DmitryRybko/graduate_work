"""DB module."""

from db.base_db import BaseDB

db: BaseDB | None = None


async def get_db():
    """Return mongo_db item."""
    return db
