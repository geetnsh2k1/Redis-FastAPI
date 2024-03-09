import uuid
from contextvars import ContextVar
from functools import wraps

from src.redis.redis_service import RedisService
from src.redis.schemas.async_request_info import AsyncRequestInfo
from src.redis.service.async_request_info_service import AsyncRequestInfoService
from src.redis.utils.constants import RedisServiceTypes
from src.redis.utils.helpers import create_async_request_info

async_request_context: ContextVar[AsyncRequestInfo] = ContextVar("async_request_context")


def async_redis_api_interceptor(route_function):
    @wraps(route_function)
    async def wrapper(*args, **kwargs):
        # 1. get the current_user details from the kwargs
        # current_user: UserDetails = kwargs.get("current_user")
        current_user_id: str = str(uuid.uuid4())

        # 2. get the redis_service from the kwargs to use redis here.
        redis_service: RedisService = kwargs.get("redis_service")

        # 3. create a new request info data for the particular api hit
        async_request_info: AsyncRequestInfo = create_async_request_info(
            user_id=current_user_id
        )

        # 4. save the request info to the particular request context so that to return the response
        async_request_context.set(async_request_info)

        # 5. add the request info to redis in order to support polling

        # 5.1 get the async request info service using the available redis service
        async_request_info_service: AsyncRequestInfoService = redis_service.get_service(
            RedisServiceTypes.ASYNC_REQUEST_INFO
        )

        # 5.2 add the data to redis using the async_request_info_service
        await async_request_info_service.add(
            data=async_request_info
        )

        return await route_function(*args, **kwargs)

    return wrapper
