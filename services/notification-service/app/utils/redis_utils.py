from app.extensions import redis_client


# ---------- AUTH CACHING ----------
def cache_auth_token(token, client_id, ttl=3600):
    redis_client.set(f"auth:token:{token}", client_id, ex=ttl)


def get_cached_client_id(token):
    key = f"auth:token:{token}"
    client_id = redis_client.get(key)
    return client_id


# ---------- RATE LIMITING ----------
def increment_rate_limit(token, window=60):
    key = f"rate_limit:{token}"
    if redis_client.exists(key):
        redis_client.incr(key)
    else:
        redis_client.set(key, 1, ex=window)
    return int(redis_client.get(key))


def is_rate_limited(token, limit):
    current = redis_client.get(f"rate_limit:{token}")
    return int(current) >= limit if current else False


# ---------- USER PREF CACHING ----------
def cache_user_pref(user_id, client_id, prefs, ttl=1800):
    key = f"pref:{user_id}:{client_id}"
    redis_client.set(key, prefs, ex=ttl)


def get_cached_user_pref(user_id, client_id):
    key = f"pref:{user_id}:{client_id}"
    val = redis_client.get(key)
    return val
