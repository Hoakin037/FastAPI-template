from asyncio import sleep
from datetime import timedelta

import pytest

from app.config.settings import RedisSettings
from app.infrastructure.cache.redis import create_redis_client
from app.shared.repositories import RedisBaseRepository

TEST_STR_VALUE: str = "Test value"
TEST_BYTES_VALUE: bytes = b"Test bytes"

TEST_PREFIX = "prefix:"
TEST_KEY_1 = "key1"
TEST_KEY_2 = "key2"


@pytest.fixture
async def get_redis_repo():
    settings = RedisSettings()
    redis_client = create_redis_client(settings)
    yield RedisBaseRepository(redis_client)

    await redis_client.aclose()


async def test_set_instance(get_redis_repo):
    repo = get_redis_repo
    await repo.set_instance(key=TEST_KEY_1, value=TEST_STR_VALUE)

    result = await repo.get_instance(key=TEST_KEY_1)
    assert result == TEST_STR_VALUE


async def test_set_bytes_instance(get_redis_repo):
    repo = get_redis_repo
    await repo.set_instance(key=TEST_KEY_1, value=TEST_BYTES_VALUE)
    result = await repo.get_instance(key=TEST_KEY_1)

    assert result == TEST_BYTES_VALUE.decode("utf-8")


async def test_change_instance(get_redis_repo):
    repo = get_redis_repo

    await repo.set_instance(key=TEST_KEY_1, value=TEST_STR_VALUE)
    await repo.set_instance(key=TEST_KEY_1, value=TEST_BYTES_VALUE)

    result = await repo.get_instance(key=TEST_KEY_1)
    assert result == TEST_BYTES_VALUE.decode("utf-8")


async def test_set_instance_with_expire(get_redis_repo):
    repo = get_redis_repo

    await repo.set_instance(
        key=TEST_KEY_2, value=TEST_STR_VALUE, expire_time=timedelta(seconds=1)
    )

    await sleep(1)

    result = await repo.get_instance(key=TEST_KEY_2)
    assert result is None


async def test_delete_instance(get_redis_repo):
    repo = get_redis_repo

    await repo.delete_instance(key=TEST_KEY_1)
    result = await repo.get_instance(key=TEST_KEY_1)

    assert result is None


async def test_delete_by_prefix(get_redis_repo):
    repo = get_redis_repo

    await repo.set_instance(key=f"{TEST_PREFIX}{TEST_KEY_1}", value=TEST_STR_VALUE)
    await repo.set_instance(key=f"{TEST_PREFIX}{TEST_KEY_2}", value=TEST_STR_VALUE)
    await repo.delete_by_prefix(prefix=TEST_PREFIX)

    result_1 = await repo.get_instance(key=TEST_KEY_1)
    result_2 = await repo.get_instance(key=TEST_KEY_2)

    assert result_1 is None
    assert result_2 is None


async def test_existance(get_redis_repo):
    repo = get_redis_repo

    await repo.set_instance(key=TEST_KEY_1, value=TEST_STR_VALUE)
    exist = await repo.check_existence(key=TEST_KEY_1)

    assert exist is True
