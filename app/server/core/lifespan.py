from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.storages.postgres import set_session_factory


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_factory = set_session_factory()

    yield

    async with app.state.session_factory() as session:
        await session.close()
