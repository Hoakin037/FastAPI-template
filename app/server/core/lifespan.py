from contextlib import asynccontextmanager

from fastapi import FastAPI
from postgres import create_engine, create_session_factory

from app.config.settings import Settings
from app.infrastructure.cache.redis import create_redis_client
from app.infrastructure.storage.s3 import create_s3_client


class Container:
    def __init__(self):
        self.settings = Settings()
        self.engine = create_engine(self.settings.postgres)
        self.session_factory = create_session_factory(self.engine)
        self.redis = create_redis_client(self.settings.redis)
        self.s3 = create_s3_client(self.settings.s3)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()

    app.state.container = container
    app.state.session_factory = container.session_factory
    app.state.redis = container.redis
    app.state.s3 = container.s3

    yield

    await container.engine.dispose()
