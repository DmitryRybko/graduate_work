
import json

import redis
from fastapi import Depends
from recommendation_service.config import settings
from loguru import logger

import redis

from db.redis import get_redis


def retrieve_recom_movies(
    user_id: str, r: redis.Redis | None = Depends(get_redis)
):
    # create a Redis client
    if user_id is None:
        movies = ["some general movie 1", "some general movie 2"]

    else:
        try:
            # retrieve the uuids list from Redis
            movies_str = r.get(user_id).decode('utf-8')
            if movies_str is None:
                movies = ["some movie 1", "some movie 2"]
            else:
                movies = json.loads(movies_str)
        except (redis.exceptions.ResponseError, AttributeError):
            movies = ["some movie 1", "some movie 2"]

    # return the recommended movies list
    return movies


if __name__ == "__main__":
    # example usage
    user_id = "email2@emails.ru"
    movies = retrieve_recom_movies(user_id)
    logger.debug(f"movies got from Redis: {movies}")
