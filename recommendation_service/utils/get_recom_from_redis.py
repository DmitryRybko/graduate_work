import redis
from config import settings


def retrieve_recom_movies(user_id):
    # create a Redis client
    if user_id == None:
        uuids = ["some movie 1", "some movie 2"]

    else:
        r = redis.Redis(settings.redis_host, settings.redis_port, settings.redis_db)

        try:
            # retrieve the uuids list from Redis
            uuids_str = r.get(user_id).decode('utf-8')
            if uuids_str is None:
                uuids = ["some movie 1", "some movie 2"]
            else:
                uuids = eval(uuids_str)
        except (redis.exceptions.ResponseError, AttributeError):
            uuids = ["some movie 1", "some movie 2"]

    # return the recommended movies list
    return uuids


if __name__ == "__main__":
    # example usage
    user_id = "email2@emails.ru"
    uuids = retrieve_recom_movies(user_id)
    print(uuids)
    print(uuids[0])
