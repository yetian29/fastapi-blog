from abc import ABC, abstractmethod

from src.domain.review.entities import Review


class IReviewService(ABC):
    @abstractmethod
    async def get_by_id(self, oid: str) -> Review:
        pass

    @abstractmethod
    async def get_by_user_id_and_post_id(
        self, user_id: str, post_id: str
    ) -> Review:
        pass

    @abstractmethod
    async def create(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def create_or_update(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def update(self, review: Review) -> Review:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> Review:
        pass
