from functools import wraps
from typing import Any

from src.redis.utils.helpers import validate_data


def validate_redis_data(func):
    @wraps(func)
    async def wrapper(self, data: Any, *args, **kwargs):
        schema = self.SCHEMA  # Get schema from class variable
        validated_data = validate_data(data=data, schema=schema)
        return await func(self, validated_data, *args, **kwargs)
    return wrapper
