from fastapi import FastAPI

import uvicorn

from src.controller import common_controller
from src.redis.redis_dependency_container import RedisDependencyContainer

app = FastAPI()

app.include_router(common_controller.router)

container = RedisDependencyContainer()

app.container = container

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
