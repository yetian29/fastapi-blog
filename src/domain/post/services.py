from abc import ABC, abstractmethod

from src.domain.post.entities import Post


class IPostService(ABC):
    @abstractmethod
    async def create(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def update(self, post: Post) -> Post:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> Post:
        pass

    @abstractmethod
    async def get_by_id(self, oid: str) -> Post:
        pass

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> list[Post]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass
