from fastapi import Request

from .client import S3Client


def get_s3_client(request: Request) -> S3Client:
    return request.app.state.container.s3
