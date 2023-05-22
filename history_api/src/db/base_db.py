"""BaseDB interface."""

import abc


class BaseDB(abc.ABC):
    """Base class to work with DB."""

    @abc.abstractmethod
    def get_history_for_user(self, user_id: str):
        """Get records for a user by user_id."""
        pass

    def get_last_1000_records_for_user(self, user_id: str):
        """Get the latest 1000 records for a user by user_id."""
        pass
