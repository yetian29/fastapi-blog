from src.helper.errors import BaseDomainException


class BaseUserException(BaseDomainException):
    pass


class UserNotFoundException(BaseUserException):
    pass


class CreateUserNotSuccessException(BaseUserException):
    pass


class UpdateUserNotSuccessException(BaseUserException):
    pass

class GetOrCreateUserNotSuccessException(BaseUserException):
    pass