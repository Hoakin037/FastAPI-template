import pytest

from app.config.settings import S3Settings
from app.infrastructure.storage.s3 import create_s3_client
from app.shared.repositories import S3BaseRepository


@pytest.fixture
async def s3_connection():
    settings = S3Settings()
    return create_s3_client(settings)


class FakeBody:
    def __init__(self, data: bytes):
        self.data = data

    async def read(self) -> bytes:
        return self.data


class FakeRawS3Client:
    def __init__(self):
        self.objects: dict[tuple[str, str], bytes] = {}
        self.metadata: dict[tuple[str, str], dict[str, str]] = {}
        self.deleted_batches: list[dict] = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return None

    async def put_object(self, Bucket: str, Key: str, Body: bytes) -> None:  # noqa: N803
        self.objects[(Bucket, Key)] = Body

    async def get_object(self, Bucket: str, Key: str) -> dict:  # noqa: N803
        return {"Body": FakeBody(self.objects[(Bucket, Key)])}

    async def head_object(self, Bucket: str, Key: str) -> dict:  # noqa: N803
        return {"Metadata": self.metadata.get((Bucket, Key), {})}

    async def delete_object(self, Bucket: str, Key: str) -> None:  # noqa: N803
        self.objects.pop((Bucket, Key), None)

    async def delete_objects(self, Bucket: str, Delete: dict) -> None:  # noqa: N803
        self.deleted_batches.append({"Bucket": Bucket, "Delete": Delete})
        for obj in Delete["Objects"]:
            self.objects.pop((Bucket, obj["Key"]), None)

    async def copy_object(
        self,
        Bucket: str,  # noqa: N803
        CopySource: dict,  # noqa: N803
        Key: str,  # noqa: N803
    ) -> None:
        self.objects[(Bucket, Key)] = self.objects[
            (CopySource["Bucket"], CopySource["Key"])
        ]


class FakeS3Client:
    def __init__(self):
        self.raw_client = FakeRawS3Client()

    def get_raw_client(self) -> FakeRawS3Client:
        return self.raw_client


@pytest.fixture
def s3_repo():
    return S3BaseRepository(FakeS3Client())


async def test_put_and_get_object(s3_repo):
    key = await s3_repo.put_object("bucket", "file.txt", b"content")
    data = await s3_repo.get_object("bucket", key)

    assert key == "file.txt"
    assert data == b"content"


async def test_get_head_object_returns_metadata(s3_repo):
    s3_repo.client.raw_client.metadata[("bucket", "file.txt")] = {
        "content-type": "text"
    }

    metadata = await s3_repo.get_head_object("bucket", "file.txt")

    assert metadata == {"content-type": "text"}


async def test_get_objects_batch_returns_existing_objects(s3_repo):
    await s3_repo.put_object("bucket", "file-1.txt", b"content-1")
    await s3_repo.put_object("bucket", "file-2.txt", b"content-2")

    result = await s3_repo.get_objects_batch(
        "bucket", ["file-1.txt", "missing.txt", "file-2.txt"]
    )

    assert result == {
        "file-1.txt": b"content-1",
        "file-2.txt": b"content-2",
    }


async def test_delete_object_removes_object(s3_repo):
    await s3_repo.put_object("bucket", "file.txt", b"content")

    await s3_repo.delete_object("bucket", "file.txt")

    assert ("bucket", "file.txt") not in s3_repo.client.raw_client.objects


async def test_delete_objects_batch_uses_quiet_delete(s3_repo):
    await s3_repo.put_object("bucket", "file-1.txt", b"content-1")
    await s3_repo.put_object("bucket", "file-2.txt", b"content-2")

    await s3_repo.delete_objects_batch(
        "bucket", [{"Key": "file-1.txt"}, {"Key": "file-2.txt"}]
    )

    assert s3_repo.client.raw_client.deleted_batches == [
        {
            "Bucket": "bucket",
            "Delete": {
                "Objects": [{"Key": "file-1.txt"}, {"Key": "file-2.txt"}],
                "Quiet": True,
            },
        }
    ]
    assert s3_repo.client.raw_client.objects == {}


async def test_copy_object_copies_data_to_new_key(s3_repo):
    await s3_repo.put_object("bucket", "source.txt", b"content")

    await s3_repo.copy_object("bucket", "source.txt", "copy.txt")

    assert await s3_repo.get_object("bucket", "copy.txt") == b"content"
