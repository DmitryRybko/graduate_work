"""Logger module."""

import logging
import sys

from settings import settings

logger: logging.Logger = logging.getLogger(__name__)


def set_log_settings() -> logging.Logger:
    """Set log level."""
    if settings.log_level == 'ERROR':
        log_level = logging.ERROR
    elif settings.log_level == 'DEBUG':
        log_level = logging.DEBUG
    else:
        log_level = logging.CRITICAL

    # log settings
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_logger() -> logging.Logger | None:
    return logger
