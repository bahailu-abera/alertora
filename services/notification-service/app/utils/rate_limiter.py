from functools import wraps
from flask import request, jsonify
from app.extensions import redis_client


def rate_limit(limit: int, window: int = 60):
    """
    limit = max requests
    window = time window in seconds
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization", "").replace(
                "Bearer ", ""
            )
            if not token:
                return jsonify({"error": "Missing token"}), 401

            key = f"rate_limit:{token}"
            current = redis_client.get(key)

            if current and int(current) >= limit:
                return jsonify({"error": "Rate limit exceeded"}), 429

            if current:
                redis_client.incr(key)
            else:
                redis_client.set(key, 1, ex=window)

            return f(*args, **kwargs)

        return wrapper

    return decorator
