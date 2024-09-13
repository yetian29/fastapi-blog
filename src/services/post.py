from dataclasses import dataclass

from src.domain.post.entities import Post
from src.domain.post.services import IPostService
from src.infrastructure.dto.post import PostDto
from src.infrastructure.repositories.post import IPostRepository


@dataclass
class PostService(IPostService):
    repository: IPostRepository

    async def get_by_id(self, oid: str) -> Post:
        dto = await self.repository.get_by_id(oid)
        return dto.to_entity()

    async def create(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.update(dto)
        return dto.to_entity()

    async def delete(self, oid: str) -> Post:
        post = await self.get_by_id(oid)
        await self.repository.delete(oid)
        return post

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> list[Post]:
        dto_iter = self.repository.find_many(
            sort_field, sort_order, limit, offset, search
        )
        return [dto.to_entity() async for dto in dto_iter]

    async def count_many(self, search: str | None = None) -> int:
        return await self.repository.count_many(search)
