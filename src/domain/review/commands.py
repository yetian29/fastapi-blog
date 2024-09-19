from dataclasses import dataclass

from src.domain.review.entities import Review


@dataclass
class CreateReviewCommand:
    review: Review


@dataclass
class UpdateReviewCommand:
    review: Review


@dataclass
class DeleteReviewCommand:
    oid: str


@dataclass
class GetReviewCommand:
    oid: str
