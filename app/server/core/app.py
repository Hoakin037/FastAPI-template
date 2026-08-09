from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import ProjectSettings
from app.infrastructure.storage.postgres.session import get_db_session
from app.server.core.lifespan import lifespan
from app.server.core.router import api


def custom_generate_unique_id(route: APIRoute) -> str:
    return route.name


settings = ProjectSettings()

app = FastAPI(
    debug=True,
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    swagger_ui_parameters={
        "docExpansion": "none",
    },
    lifespan=lifespan,
    generate_unique_id_function=custom_generate_unique_id,
)


app.include_router(api)


@app.get("/test")
async def test(session: Annotated[AsyncSession, Depends(get_db_session)]):
    await session.execute(text("INSERT INTO users (name) VALUES ('pypy') "))
    await session.commit()
