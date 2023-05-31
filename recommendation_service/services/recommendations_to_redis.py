import redis
import json
import datetime
from recommendation_service.utils.get_recommendations import get_recommendations
from recommendation_service.config import settings


def save_recommendations_for_users() -> None:
    # create a Redis client
    r: redis.Redis = redis.Redis(
        settings.redis_host, settings.redis_port, settings.redis_db
    )

    # define the data to be saved
    user_id: str = 'email2@emails.ru'
    movies: dict | None = get_recommendations(user_id)

    # convert the uuids list to a JSON-encoded string
    movies_str: str = json.dumps(movies)

    # save the data to Redis
    r.set(user_id, movies_str)


# set up a weekly timer to run the function
week_interval = datetime.timedelta(weeks=1)
last_run_time = datetime.datetime.now()

while True:
    current_time = datetime.datetime.now()
    if (current_time - last_run_time) >= week_interval:
        save_recommendations_for_users()
        last_run_time = current_time