
import json
import redis
from loguru import logger

from recommendation_service.services.recommendations_to_redis import save_recommendations_for_users
from recommendation_service.config import settings


def retrieve_recom_movies(user_id: str):
    # create a Redis client

    r = redis.Redis(host=settings.redis_host, port=settings.redis_port)

    if user_id is None:
        movies = {"some movie 1": {"description": "movie description"}}

    else:
        try:
            # retrieve movie data from Redis
            movies_str = r.get(user_id).decode('utf-8')
            logger.debug(f"retrieving from Redis")
            if movies_str is None:
                logger.debug(f"no movies in Redis")
                save_recommendations_for_users(user_id)
                movies = {"some movie from Redis": {"description": "movie description"}}
            else:
                logger.debug(f"movies taken from Redis")
                movies = json.loads(movies_str)
        except (redis.exceptions.ResponseError, AttributeError) as e:
            logger.error(f"Redis related error: {e}")
            movies = {"some movie - exception in redis": {"description": "movie description"}}

    # return the recommended movies list
    return movies


if __name__ == "__main__":
    # example usage
    user_id = "email2@emails.ru"
    movies = retrieve_recom_movies(user_id)
    logger.debug(f"movies got from Redis: {movies}")
