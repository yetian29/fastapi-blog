from src.helper.errors import BaseDomainException


class BaseReviewException(BaseDomainException):
    pass


class CreateReviewNotSuccessException(BaseReviewException):
    pass


class UpdateReviewNotSuccessException(BaseReviewException):
    pass


class ReviewNotFoundException(BaseReviewException):
    pass
