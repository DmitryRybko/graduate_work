import redis
import json
from recommendation_service.utils.get_recommendations import get_viewed_movies

from recommendation_service.config import settings

# create a Redis client
r = redis.Redis(settings.redis_host, settings.redis_port, settings.redis_db)

# define the data to be saved
user_id = 'email2@emails.ru'
uuids = get_viewed_movies(user_id)


# convert the uuids list to a JSON-encoded string
uuids_str = json.dumps(uuids)

# save the data to Redis
r.set(user_id, uuids_str)
