import datetime
import json

from fastapi import Depends

import redis

from db.redis import get_redis
from utils.get_recommendations import get_recommendations


def save_recommendations_for_users(r: redis.Redis | None = Depends(get_redis)):
    # define the data to be saved

    user_id: str = 'email2@emails.ru'
    movies: dict | None = get_recommendations(user_id)


    # convert the uuids list to a JSON-encoded string
    movies_str: str = json.dumps(movies)

    # save the data to Redis
    if r:
        r.set(user_id, movies_str)
    else:
        raise Exception('Redis is not available')


# set up a weekly timer to run the function
week_interval = datetime.timedelta(weeks=1)
last_run_time = datetime.datetime.now()

while True:
    current_time = datetime.datetime.now()
    if (current_time - last_run_time) >= week_interval:
        save_recommendations_for_users()
        last_run_time = current_time
