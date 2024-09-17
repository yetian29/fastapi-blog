from dataclasses import dataclass

from src.domain.review.entities import Review


@dataclass
class CreateOrUpdateReviewCommand:
    user_token: str
    review: Review


@dataclass
class DeleteReviewCommand:
    oid: str
