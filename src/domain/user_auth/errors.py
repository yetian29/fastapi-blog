from src.domain.base.errors import BaseDomainException


class CodeIsNotFoundException(BaseDomainException):
    pass


class CodesAreNotEqualException(BaseDomainException):
    pass


class CodeHasExpiredException(BaseDomainException):
    pass


class UserAuthIsNotFoundException(BaseDomainException):
    pass
