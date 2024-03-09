from typing import Union

from redis.asyncio import Redis

from src.redis.service.async_request_info_service import AsyncRequestInfoService
from src.redis.utils.constants import RedisServiceTypes


class RedisService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def get_service(self, service_type: RedisServiceTypes) -> Union[AsyncRequestInfoService]:
        if service_type.__eq__(RedisServiceTypes.ASYNC_REQUEST_INFO):
            return AsyncRequestInfoService(redis=self._redis)
        else:
            raise ValueError("Unknown service type")
