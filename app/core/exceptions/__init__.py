from http import HTTPStatus
from logging import getLogger

from fastapi import HTTPException

logger = getLogger(__name__)


class APIBaseException(HTTPException):
    """
    Base class for all API exceptions.
    """

    status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code = "INTERNAL_SERVER_ERROR"
    error_description = "An unexpected error occurred"

    def __init__(
        self,
        message: str | None = None,
        status_code: HTTPStatus | int | None = None,
        extra_log: str | None = None,
    ):
        self.message = message or self.error_description
        self.status_code = status_code or self.status_code

        if extra_log:
            logger.exception(extra_log)

        status_code_int: int = int(
            self.status_code.value
            if isinstance(self.status_code, HTTPStatus)
            else self.status_code
        )

        super().__init__(status_code=status_code_int, detail=self.message)
