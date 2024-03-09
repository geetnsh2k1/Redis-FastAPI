import asyncio

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from src.dto.response.async_api_response import AsyncRequestInfoResponse
from src.factory.service_factory import ServiceFactory
from src.redis.decorators.async_redis_api_interceptor import async_redis_api_interceptor, async_request_context
from src.redis.redis_dependency_container import RedisDependencyContainer
from src.redis.redis_service import RedisService

router = APIRouter()


@router.get(
    path="/get-async",
    summary="Retrieve details of an asynchronous API request using the specified request ID.",
    response_model=AsyncRequestInfoResponse,
    tags=["COMMON"]
)
@inject
async def get_async_api_details(
        request_id: str,
        redis_service: RedisService = Depends(Provide[RedisDependencyContainer.redis_service])
):
    return AsyncRequestInfoResponse(
        status_code=status.HTTP_200_OK,
        message="ASYNC API REQUEST DETAILS SUCCESSFULLY FETCHED",
        data=await ServiceFactory.get_common_service().get_async_api_details(
            request_id=request_id,
            redis_service=redis_service
        )
    )


@router.get(
    path="/test-async",
    response_model=AsyncRequestInfoResponse,
    tags=["COMMON"]
)
@inject
@async_redis_api_interceptor
async def test_async_api(
        redis_service: RedisService = Depends(Provide[RedisDependencyContainer.redis_service])
):
    async_request_info = async_request_context.get()  # Access request from the request context

    asyncio.create_task(
        ServiceFactory.get_common_service().process(
            request_id=async_request_info.request_id,
            redis_service=redis_service,
        )
    )

    return AsyncRequestInfoResponse(
        status_code=status.HTTP_201_CREATED,
        message="ASYNC API REQUEST SUCCESSFULLY CREATED",
        data=async_request_info
    )
