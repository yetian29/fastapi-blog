
from src.helper.errors import BaseServiceException


class BaseCodeException(BaseServiceException):
    pass


class CodeNotFoundException(BaseCodeException):
    pass

class CodesNotEqualException(BaseCodeException):
    pass

class CodeExpiredException(BaseCodeException):
    pass