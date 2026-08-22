from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


def create_session_factory(engine: AsyncEngine):
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )
