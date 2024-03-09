from dependency_injector import containers, providers

from src.redis.redis_pool_initializer import init_redis_pool
from src.redis.redis_service import RedisService


class RedisDependencyContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.controller.common_controller",
        ]
    )

    redis_pool = providers.Resource(
        init_redis_pool,
        host="localhost",
        port="6379",
    )

    redis_service = providers.Factory(
        RedisService,
        redis=redis_pool,
    )
