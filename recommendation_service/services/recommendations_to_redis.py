import datetime
import json

from fastapi import Depends

import redis

from recommendation_service.db.redis import get_redis
from recommendation_service.utils.get_recommendations import get_recommendations


def save_recommendations_for_users(user: str, r: redis.Redis | None = Depends(get_redis)):

    user_id: str = user
    movies: dict | None = get_recommendations(user_id)

    # convert the uuids list to a JSON-encoded string
    movies_str: str = json.dumps(movies)

    # save the data to Redis
    if r:
        r.set(user_id, movies_str)
    else:
        raise Exception('Redis is not available')
