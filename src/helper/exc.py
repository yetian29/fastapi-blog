from typing import Optional


class BaseException(Exception):
    def __init__(self, message: Optional[str] = None, *args) -> None:
        self.message = message
        super().__init__(message, *args)


class BaseDomainException(BaseException):
    pass


class BaseApplicationException(BaseException):
    pass
