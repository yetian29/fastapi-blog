from src.helper.errors import BaseDomainException


class BasePostException(BaseDomainException):
    pass


class PostNotFoundException(BasePostException):
    pass


class CreatePostNotSuccessException(BasePostException):
    pass


class UpdatePostNotSuccessException(BasePostException):
    pass


class DeletePostNotSuccessException(BasePostException):
    pass
