from src.helper.errors import BaseDomainException


class BaseUserProfileException(BaseDomainException):
    pass


class UserProfileNotFoundException(BaseUserProfileException):
    pass


class CreateUserProfileNotSuccessException(BaseUserProfileException):
    pass


class UpdateUserProfileNotSuccessException(BaseUserProfileException):
    pass
