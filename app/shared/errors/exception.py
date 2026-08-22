from enum import Enum

from fastapi import HTTPException
from starlette.responses import JSONResponse

from .base_error_schema import ExceptionModel


class BackendException(HTTPException):
    def __init__(self, error: Enum | ExceptionModel):
        if isinstance(error, ExceptionModel):
            self.error_value = error
        else:
            self.error_value: ExceptionModel = error.value()

        self.status_code = self.error_value.http_status

    def __str__(self):
        return f"{self.error_value.code}"

    def __repr__(self):
        return f"{self.error_value.code}"

    def response(self):
        return JSONResponse(
            self.error_value.model_dump(by_alias=True), status_code=self.status_code
        )
