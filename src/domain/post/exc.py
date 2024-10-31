from src.domain.base.exc import BaseApplicationException


class BasePostException(BaseApplicationException):
    pass


class PostNotFoundException(BasePostException):
    pass


class PostsNotFoundException(BasePostException):
    pass
