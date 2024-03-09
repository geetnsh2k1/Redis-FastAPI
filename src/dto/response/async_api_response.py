from pydantic import Field

from src.dto.api_response import Response
from src.redis.schemas.async_request_info import AsyncRequestInfo


class AsyncRequestInfoResponse(Response):
    data: AsyncRequestInfo = Field(
        ...,
        description="Async Request Info details"
    )
