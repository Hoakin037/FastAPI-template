from __future__ import annotations

from functools import reduce
from operator import or_
from typing import TYPE_CHECKING, Any

from app.infrastructure.logger import setup_logging

if TYPE_CHECKING:
    from enum import Enum

logger = setup_logging(__name__)

_REQUIRED_METHOD = "get_error_response"


def _validate_error_class(error_class: type) -> None:
    method = getattr(error_class, _REQUIRED_METHOD, None)
    if not callable(method):
        error = f"Invalid error passed. Error class must be a subclass of ExceptionModel and should have '{_REQUIRED_METHOD}' method"
        raise TypeError(error)


def _extract_error_response(error: Enum) -> tuple[int, dict[str, Any]]:
    error_class = error.value
    _validate_error_class(error_class)

    return error_class.get_error_response()


def _collect_errors_data(
    errors: list[Enum],
) -> tuple[set[int], list[type], list[str]]:
    codes: set[int] = set()
    models: list[type] = []
    descriptions: list[str] = []

    for error in errors:
        code, body = _extract_error_response(error)
        codes.add(code)
        models.append(body["model"])
        descriptions.append(body.get("description", ""))

    return codes, models, descriptions


def _merge_same_status_errors(errors: list[Enum]) -> dict[int, dict[str, Any]]:
    codes, models, descriptions = _collect_errors_data(errors)

    if len(codes) > 1:
        sorted_codes = ", ".join(map(str, sorted(codes)))
        raise ValueError(f"Errors are not compatible: {sorted_codes}")  # noqa: EM102

    code = codes.pop()
    merged_model = reduce(or_, models)
    merged_description = " | ".join(filter(None, descriptions))

    return {code: {"model": merged_model, "description": merged_description}}


def _process_single_error(error: Enum) -> dict[int, dict[str, Any]]:
    code, body = _extract_error_response(error)
    return {code: body}


def generate_responses_from_errors(
    *args: Enum | list[Enum],
) -> dict[int | str, dict[str, Any]]:
    result: dict[int | str, dict[str, Any]] = {}

    for item in args:
        response = (
            _merge_same_status_errors(item)
            if isinstance(item, list)
            else _process_single_error(item)
        )

        for code, body in response.items():
            if code in result:
                logger.warning(
                    "OpenAPI response for HTTP status %s is being overwritten: "
                    "previous_model=%r, new_model=%r",
                    code,
                    result[code].get("model"),
                    body.get("model"),
                )
            result[code] = body

    return result
