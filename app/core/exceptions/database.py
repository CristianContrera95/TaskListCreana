from http import HTTPStatus

from app.core.exceptions import APIBaseException


class NotFound(APIBaseException):
    status_code = HTTPStatus.NOT_FOUND
    error_code = "NOT_FOUND"
