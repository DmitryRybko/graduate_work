import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379)

# Get all keys in the database
keys = r.keys()

# Print all data in the database
for key in keys:
    print(key.decode('utf-8'), r.get(key).decode('utf-8'))