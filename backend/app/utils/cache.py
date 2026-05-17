import json
from typing import TypeVar

from pydantic import BaseModel
from redis import Redis

T = TypeVar("T", bound=BaseModel)


def get_model(redis: Redis, key: str, model: type[T]) -> T | None:
    payload = redis.get(key)
    if not payload:
        return None
    return model.model_validate_json(payload)


def set_model(redis: Redis, key: str, value: BaseModel, ttl_seconds: int) -> None:
    redis.setex(key, ttl_seconds, value.model_dump_json())


def set_json(redis: Redis, key: str, value: object, ttl_seconds: int) -> None:
    redis.setex(key, ttl_seconds, json.dumps(value, default=str))
