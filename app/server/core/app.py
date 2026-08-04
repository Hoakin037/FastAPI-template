from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.storages.postgres.core.session import get_db_session
from app.server.core.lifespan import lifespan

app = FastAPI(lifespan=lifespan)


@app.get("/test")
async def test(session: Annotated[AsyncSession, Depends(get_db_session)]): ...
