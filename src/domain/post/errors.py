from src.domain.base.errors import BaseDomainException


class PostNotFoundException(BaseDomainException):
    pass


class PostsNotFoundException(BaseDomainException):
    pass
