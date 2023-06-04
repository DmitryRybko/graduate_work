"""BaseDB interface."""

import abc


class BaseDB(abc.ABC):
    """Base class to work with DB."""

    @abc.abstractmethod
    def get_history_for_user(self, user_id: str, limit: int):
        """Get records for a user by user_id."""
        pass

    @abc.abstractmethod
    def add_history_record(self, user_id: str, film_id: str):
        """Create new record with user_id and film_id."""
        pass
