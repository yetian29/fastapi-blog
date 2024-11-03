from src.helper.exc import BaseApplicationException


class BaseServiceException(BaseApplicationException):
    pass


# Post
class PostNotFoundException(BaseServiceException):
    pass


class PostsNotFoundException(BaseServiceException):
    pass


# User Auth
class CodeIsNotFoundException(BaseServiceException):
    pass


class CodesAreNotEqualException(BaseServiceException):
    pass


class CodeHasExpiredException(BaseServiceException):
    pass


class UserAuthIsNotFoundException(BaseServiceException):
    pass
