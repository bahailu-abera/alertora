from redis import Redis


mongo_database = None
redis_client = Redis(host="redis", port=6379, decode_responses=True)
