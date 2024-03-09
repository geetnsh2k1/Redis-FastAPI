import json
import uuid
from typing import Type, Union, Any

from pydantic import BaseModel, ValidationError

from src.redis.schemas.async_request_info import AsyncRequestInfo
from src.redis.utils.constants import AsyncRequestStatus


def generate_request_id() -> str:
    return str(uuid.uuid4())


def create_async_request_info(user_id: str) -> AsyncRequestInfo:
    return AsyncRequestInfo(
        request_id=generate_request_id(),
        status=AsyncRequestStatus.PROCESSING,
        requested_by=user_id
    )


def validate_data(data: Any, schema: Type[BaseModel]) -> Union[BaseModel, None]:
    try:
        validated_data = schema(**data.dict())
        return validated_data
    except ValidationError as e:
        print("[Validation-Failed]", e)
        raise e


def convert_dict_to_model(data: dict, schema: Type[BaseModel]) -> Union[BaseModel, None]:
    try:
        return schema(**data)
    except (ValidationError, json.JSONDecodeError) as e:
        raise ValueError(f"Failed to convert JSON string to data: {e}")


def preprocess_data_for_redis(update_data: Any) -> dict:
    processed_data = {}
    for field, value in update_data.dict().items():
        # Only include values that are not None
        if value is not None:
            processed_data[field] = value
    return processed_data


def convert_model_to_json_string(_object: BaseModel) -> str:
    return json.dumps(
        _object.model_dump(mode="json")
    )
