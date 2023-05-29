import redis
import json

from recommendation_service.utils.get_recommendations import get_recommendations
from recommendation_service.config import settings

# create a Redis client
r = redis.Redis(settings.redis_host, settings.redis_port, settings.redis_db)

# define the data to be saved
user_id = 'email2@emails.ru'
movies = get_recommendations(user_id)


# convert the uuids list to a JSON-encoded string
movies_str = json.dumps(movies)

# save the data to Redis
r.set(user_id, movies_str)
