"""DB redis module."""

import redis


def get_redis():
    """Return Redis object to work with FastAPI."""
    redis_conn = redis.Redis(host='localhost', port=6379)
    return redis_conn