from redis import Redis

from app.core.config import get_settings


def get_redis() -> Redis:
    return Redis.from_url(get_settings().resolved_redis_url, decode_responses=True)
