from src.domain.base.errors import BaseDomainException


class ReviewIsNotFoundException(BaseDomainException):
    pass


class ReviewsIsNotFoundException(BaseDomainException):
    pass
