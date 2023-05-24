import redis
import json

# create a Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# define the data to be saved
user_id = '12345'
uuids = ['a1b2c3', 'd4e5f6', 'g7h8i9']

# convert the uuids list to a JSON-encoded string
uuids_str = json.dumps(uuids)

# save the data to Redis
r.set(user_id, uuids_str)
