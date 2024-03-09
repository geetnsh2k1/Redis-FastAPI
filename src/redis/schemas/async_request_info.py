from datetime import datetime
import re
from typing import Optional, Any

from pydantic import BaseModel, Field, field_validator

from src.redis.utils.constants import AsyncRequestStatus


class AsyncRequestInfo(BaseModel):
    request_id: str = Field(..., description="A unique identifier for each request.")
    status: AsyncRequestStatus = Field(..., description="The current status of the request.")
    response: Optional[Any] = Field("", description="The execution response of the api.")
    error: Optional[Any] = Field("", description="Error while executing async api.")
    start_time: Optional[str] = Field(datetime.now().isoformat(), description="Timestamp indicating when the "
                                                                              "execution started.")
    end_time: Optional[str] = Field("", description="Timestamp indicating when the execution ended.")
    requested_by: str = Field(..., description="User-Id of the requested user.")

    @field_validator("request_id")
    def validate_request_id_format(cls, value):
        if value:
            request_id_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(request_id_pattern, value):
                raise ValueError("Invalid request-id format")
        return value

    @field_validator("request_id")
    def validate_requested_by_format(cls, value):
        if value:
            validate_requested_by_format = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
            if not re.match(validate_requested_by_format, value):
                raise ValueError("Invalid user-id format")
        return value


class AsyncRequestInfoUpdate(BaseModel):
    status: Optional[AsyncRequestStatus] = Field(None, description="The current status of the request.")
    response: Optional[Any] = Field(None, description="The execution response of the api.")
    error: Optional[Any] = Field(None, description="Error while executing async api.")
    end_time: Optional[str] = Field(None, description="Timestamp indicating when the execution ended.")
