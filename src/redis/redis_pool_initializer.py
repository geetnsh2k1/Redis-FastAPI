from typing import AsyncIterator

from redis.asyncio import Redis, from_url


async def init_redis_pool(host: str, port: str) -> AsyncIterator[Redis]:
    session = from_url(f"redis://{host}:{port}", encoding="utf-8", decode_responses=True)
    yield session
    session.close()
    await session.wait_closed()
