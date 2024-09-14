from dataclasses import dataclass

from src.domain.review.entities import Review


@dataclass
class CreateOrUpdateReviewCommand:
    review: Review


@dataclass
class DeleteReviewCommand:
    oid: str
