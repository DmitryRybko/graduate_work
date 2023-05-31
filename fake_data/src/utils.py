"""Utils module."""

import logging
import sys
from time import sleep

from settings import settings


def set_log_level() -> None:
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


def wait_db(engine, tables: tuple, timeout_min: int = 2):
    """Wait when all db and all tables are available."""
    timeout = timeout_min * 60
    while timeout:
        for table in tables:
            if not engine.dialect.has_table(engine, table):
                sleep(2)
                timeout -= 2
            else:
                return
    print(f'Engine: {engine}')
    print(f'Tables: {tables}')
    raise Exception('Timeout of waiting DB.')
