from abc import ABC, abstractmethod

from src.domain.review.entitties import Review


class IReviewService(ABC):
    @abstractmethod
    async def get_by_oid(self, oid: str) -> Review:
        pass

    @abstractmethod
    async def create(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def update(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> Review:
        pass

    @abstractmethod
    async def get_review_list_by_post_id(
        self, post_id: str, sort_field: str, sort_order: int, limit: int, offset: int
    ) -> list[Review]:
        pass

    @abstractmethod
    async def count_many(self, post_id: str) -> int:
        pass
