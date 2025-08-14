from http import HTTPStatus

from app.core.exceptions import APIBaseException


class InvalidRequest(APIBaseException):
    status_code = HTTPStatus.BAD_REQUEST
    error_code = "BAD_REQUEST"
