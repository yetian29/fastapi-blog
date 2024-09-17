from dataclasses import dataclass

from src.domain.review.entities import Review


@dataclass
class CreateOrUpdateReviewCommand:
    review: Review
    user_token: str


@dataclass
class DeleteReviewCommand:
    oid: str
