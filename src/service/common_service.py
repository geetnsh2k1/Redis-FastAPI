import asyncio
from datetime import datetime

from src.redis.redis_service import RedisService
from src.redis.schemas.async_request_info import AsyncRequestInfoUpdate
from src.redis.service.async_request_info_service import AsyncRequestInfoService
from src.redis.utils.constants import RedisServiceTypes, AsyncRequestStatus
from src.redis.utils.helpers import preprocess_data_for_redis, convert_model_to_json_string


class CommonService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommonService, cls).__new__(cls)
        return cls._instance

    @staticmethod
    async def get_async_api_details(
            request_id: str,
            redis_service: RedisService
    ):
        async_request_info_service: AsyncRequestInfoService = redis_service.get_service(
            RedisServiceTypes.ASYNC_REQUEST_INFO
        )

        try:
            request_details = await async_request_info_service.get(
                request_id=request_id
            )
            return request_details
        except Exception as e:
            raise e

    @staticmethod
    async def updated_async_request_info(
            async_request_info_update: AsyncRequestInfoUpdate,
            request_id: str,
            async_request_info_service: AsyncRequestInfoService
    ):
        await async_request_info_service.update(
            request_id=request_id,
            data=preprocess_data_for_redis(
                async_request_info_update
            )
        )

    @staticmethod
    async def process(
            request_id: str,
            redis_service: RedisService
    ):
        async_request_info_service: AsyncRequestInfoService = redis_service.get_service(
            RedisServiceTypes.ASYNC_REQUEST_INFO
        )

        try:
            await asyncio.sleep(10)

            await CommonService.updated_async_request_info(
                request_id=request_id,
                async_request_info_service=async_request_info_service,
                async_request_info_update=AsyncRequestInfoUpdate(
                    end_time=datetime.now().isoformat(),
                    status=AsyncRequestStatus.EXECUTED,
                    response="sleep done"
                )
            )
        except Exception as e:
            await CommonService.updated_async_request_info(
                request_id=request_id,
                async_request_info_service=async_request_info_service,
                async_request_info_update=AsyncRequestInfoUpdate(
                    end_time=datetime.now().isoformat(),
                    status=AsyncRequestStatus.FAILED,
                    error=str(e)
                )
            )

