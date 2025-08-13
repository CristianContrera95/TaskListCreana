from http import HTTPStatus

from app.core.exceptions import APIBaseException


class UserAlreadyExists(APIBaseException):
    """
    Exception raised when trying to add a user that already exists.
    """

    status_code = HTTPStatus.CONFLICT
    error_code = "USER_ALREADY_EXISTS"
    error_description = "User already exists."


class UserNotFound(APIBaseException):
    """
    Exception raised when an invalid access credentials are provided.
    """

    status_code = HTTPStatus.UNAUTHORIZED
    error_code = "INVALID_ACCESS_CREDENTIALS"
    error_description = "Invalid access ccredentials provided."


class InvalidAccessToken(APIBaseException):
    """
    Exception raised when an invalid access token is provided.
    """

    status_code = HTTPStatus.UNAUTHORIZED
    error_code = "INVALID_ACCESS_TOKEN"
    error_description = "Invalid access token provided."
