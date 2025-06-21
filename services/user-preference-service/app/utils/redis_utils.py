from app.extensions import redis_client


def cache_user_preference(user_id, client_id, preference_data, ttl=3600):
    """
    Store user preference in Redis cache.
    """
    redis_key = f"user_pref:{user_id}:{client_id}"
    redis_client.set(redis_key, preference_data, ex=ttl)


def get_cached_user_preference(user_id, client_id):
    """
    Retrieve user preference from Redis cache.
    """
    redis_key = f"user_pref:{user_id}:{client_id}"
    return redis_client.get(redis_key)
