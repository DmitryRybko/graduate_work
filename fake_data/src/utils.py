"""Utils module."""

from time import sleep

from logger import get_logger


def wait_db(
    engine, tables: tuple, schema: str = 'public', timeout_min: int = 2
):
    """Wait when all db and all tables are available."""
    logger = get_logger()
    logger.debug(f'Engine: {engine}; Tables: {tables}; Timeout: {timeout_min}')
    timeout = timeout_min * 60
    for table in tables:
        while True:
            logger.debug(f'Table to wait {table}')
            if engine.dialect.has_table(engine, table, schema=schema):
                logger.debug(f'Table {table} is available')
                break
            sleep(2)
            timeout -= 2

            if timeout <= 0:
                raise Exception('Timeout of waiting DB.')
