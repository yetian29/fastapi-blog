from src.helper.exc import BaseApplicationException


class BasePostException(BaseApplicationException):
    pass


class PostNotFoundException(BasePostException):
    pass


class PostsNotFoundException(BasePostException):
    pass
