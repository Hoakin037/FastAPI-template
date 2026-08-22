import uuid

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.config.settings import PostgresSettings
from app.infrastructure.storage.postgres import create_engine
from app.modules.users.repositories.user_repo import UserRepo
from app.modules.users.schemas.user import UserCreate, UserUpdate

# Константы для тестов
TEST_NAME_1: str = "John"
TEST_SURNAME_1: str = "Doe"
TEST_AGE_1: int = 25

TEST_NAME_2: str = "Jane"
TEST_SURNAME_2: str = "Smith"
TEST_AGE_2: int = 30

TEST_NAME_UPDATED: str = "Johnny"
TEST_SURNAME_UPDATED: str = "UpdatedDoe"
TEST_AGE_UPDATED: int = 26

TEST_NAME_UNIQUE: str = "UniqueUser"
TEST_SURNAME_UNIQUE: str = "Unique"
TEST_AGE_UNIQUE: int = 40

TEST_NAME_OTHER: str = "OtherUser"
TEST_SURNAME_OTHER: str = "Other"
TEST_AGE_OTHER: int = 50

TEST_NON_EXISTENT_SID = uuid.uuid4()


@pytest.fixture
async def user_repo():
    settings = PostgresSettings()
    engine = create_engine(settings)

    async with engine.connect() as connection:
        trans = await connection.begin()

        session_factory = async_sessionmaker(
            bind=connection, autoflush=False, autocommit=False, expire_on_commit=False
        )

        async with session_factory() as session:
            original_commit = session.commit

            async def fake_commit():  # noqa: ANN202
                await session.flush()

            session.commit = fake_commit

            yield UserRepo(session)

            session.commit = original_commit

        await trans.rollback()


async def test_create_user(user_repo):
    repo = user_repo
    user_data = UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)

    user = await repo.create(user_data)

    assert user.sid is not None
    assert user.name == TEST_NAME_1
    assert user.surname == TEST_SURNAME_1
    assert user.age == TEST_AGE_1


async def test_create_many_users(user_repo):
    repo = user_repo
    users_data = [
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1),
        UserCreate(name=TEST_NAME_2, surname=TEST_SURNAME_2, age=TEST_AGE_2),
    ]

    users = await repo.create_many(users_data)

    assert len(users) == 2
    assert users[0].name == TEST_NAME_1
    assert users[1].name == TEST_NAME_2


async def test_get_by_sid(user_repo):
    repo = user_repo
    user_data = UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    created_user = await repo.create(user_data)

    fetched_user = await repo.get_by_sid(created_user.sid)

    assert fetched_user is not None
    assert fetched_user.sid == created_user.sid
    assert fetched_user.name == TEST_NAME_1


async def test_get_by_sid_not_found(user_repo):
    repo = user_repo

    fetched_user = await repo.get_by_sid(TEST_NON_EXISTENT_SID)
    assert fetched_user is None


async def test_get_all(user_repo):
    repo = user_repo
    user1 = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )
    user2 = await repo.create(
        UserCreate(name=TEST_NAME_2, surname=TEST_SURNAME_2, age=TEST_AGE_2)
    )

    users = await repo.get_all()
    sids = [u.sid for u in users]

    assert user1.sid in sids
    assert user2.sid in sids


async def test_get_all_with_where_clause(user_repo):
    repo = user_repo
    user1 = await repo.create(
        UserCreate(
            name=TEST_NAME_UNIQUE, surname=TEST_SURNAME_UNIQUE, age=TEST_AGE_UNIQUE
        )
    )
    await repo.create(
        UserCreate(name=TEST_NAME_OTHER, surname=TEST_SURNAME_OTHER, age=TEST_AGE_OTHER)
    )

    users = await repo.get_all(repo.model.name == TEST_NAME_UNIQUE)

    assert len(users) == 1
    assert users[0].sid == user1.sid


async def test_update_user_with_schema(user_repo):
    repo = user_repo
    user = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )

    update_data = UserUpdate(name=TEST_NAME_UPDATED, age=TEST_AGE_UPDATED)
    updated_user = await repo.update(user, update_data)

    assert updated_user.name == TEST_NAME_UPDATED
    assert updated_user.surname == TEST_SURNAME_1
    assert updated_user.age == TEST_AGE_UPDATED


async def test_update_user_with_dict(user_repo):
    repo = user_repo
    user = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )

    update_data = {"name": TEST_NAME_UPDATED}
    updated_user = await repo.update(user, update_data)

    assert updated_user.name == TEST_NAME_UPDATED
    assert updated_user.surname == TEST_SURNAME_1


async def test_update_many_users(user_repo):
    repo = user_repo
    user1 = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )
    user2 = await repo.create(
        UserCreate(name=TEST_NAME_2, surname=TEST_SURNAME_2, age=TEST_AGE_2)
    )

    pairs = [
        (user1, UserUpdate(name=TEST_NAME_UPDATED)),
        (user2, {"name": TEST_NAME_OTHER}),
    ]

    updated_users = await repo.update_many(pairs)

    assert len(updated_users) == 2
    assert updated_users[0].name == TEST_NAME_UPDATED
    assert updated_users[1].name == TEST_NAME_OTHER


async def test_delete_user(user_repo):
    repo = user_repo
    user = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )

    await repo.delete(user)

    fetched_user = await repo.get_by_sid(user.sid)
    assert fetched_user is None


async def test_delete_many_users(user_repo):
    repo = user_repo
    user1 = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )
    user2 = await repo.create(
        UserCreate(name=TEST_NAME_2, surname=TEST_SURNAME_2, age=TEST_AGE_2)
    )

    await repo.delete_by_sid(sid=[user1.sid, user2.sid])

    assert await repo.get_by_sid(user1.sid) is None
    assert await repo.get_by_sid(user2.sid) is None


async def test_delete_by_sid_single(user_repo):
    repo = user_repo
    user = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )

    await repo.delete_by_sid(user.sid)

    fetched_user = await repo.get_by_sid(user.sid)
    assert fetched_user is None


async def test_delete_by_sid_list(user_repo):
    repo = user_repo
    user1 = await repo.create(
        UserCreate(name=TEST_NAME_1, surname=TEST_SURNAME_1, age=TEST_AGE_1)
    )
    user2 = await repo.create(
        UserCreate(name=TEST_NAME_2, surname=TEST_SURNAME_2, age=TEST_AGE_2)
    )

    await repo.delete_by_sid([user1.sid, user2.sid])

    fetched1 = await repo.get_by_sid(user1.sid)
    fetched2 = await repo.get_by_sid(user2.sid)

    assert fetched1 is None
    assert fetched2 is None
