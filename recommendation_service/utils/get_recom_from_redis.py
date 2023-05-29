import redis
from recommendation_service.config import settings
from loguru import logger


def retrieve_recom_movies(user_id):
    # create a Redis client
    if user_id == None:
        movies = ["some general movie 1", "some general movie 2"]

    else:
        r = redis.Redis(settings.redis_host, settings.redis_port, settings.redis_db)

        try:
            # retrieve the uuids list from Redis
            movies_str = r.get(user_id).decode('utf-8')
            if movies_str is None:
                movies = ["some movie 1", "some movie 2"]
            else:
                movies = eval(movies_str)
        except (redis.exceptions.ResponseError, AttributeError):
            movies = ["some movie 1", "some movie 2"]

    # return the recommended movies list
    return movies


if __name__ == "__main__":
    # example usage
    user_id = "email2@emails.ru"
    movies = retrieve_recom_movies(user_id)
    logger.debug(f"movies got from Redis: {movies}")

