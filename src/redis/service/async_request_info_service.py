from typing import Optional, Any

from redis.asyncio import Redis

from src.redis.decorators.validate_redis_data import validate_redis_data
from src.redis.schemas.async_request_info import AsyncRequestInfo
from src.redis.service.base_redis_service import RedisServiceBase
from src.redis.utils.helpers import convert_dict_to_model


class AsyncRequestInfoService(RedisServiceBase):
    _instance: Optional['AsyncRequestInfoService'] = None
    SCHEMA = AsyncRequestInfo
    HASH_NAME = "async_requests_info:{request_id}"

    def __new__(cls, redis: Redis):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, redis: Redis):
        self._redis = redis

    @staticmethod
    def _get_hash_key(request_id: str) -> str:
        return AsyncRequestInfoService.HASH_NAME.format(request_id=request_id)

    @validate_redis_data
    async def add(self, data: Any):
        await self._redis.hset(
            name=self._get_hash_key(data.request_id),
            mapping=data.__dict__
        )

    async def get(self, request_id: str):
        data: dict = await self._redis.hgetall(
            self._get_hash_key(request_id)
        )
        return convert_dict_to_model(
            data=data,
            schema=self.SCHEMA
        )

    async def update(self, request_id: str, data: dict):
        await self._redis.hset(
            name=self._get_hash_key(request_id),
            mapping=data
        )
