import redis

# create a Redis client
r = redis.Redis(host='localhost', port=6379, db=0)

# define the user_id to retrieve
user_id = '12345'

# retrieve the uuids list from Redis
uuids_str = r.get(user_id).decode('utf-8')
uuids = eval(uuids_str)

# print the uuids list
print(uuids)
print(uuids[0])
