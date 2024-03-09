from enum import Enum


class RedisServiceTypes(str, Enum):
    ASYNC_REQUEST_INFO = "async_request_info"


class AsyncRequestStatus(str, Enum):
    PROCESSING = "processing"
    EXECUTED = "executed"
    FAILED = "failed"
