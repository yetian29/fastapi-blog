from dataclasses import dataclass
from typing import Optional
from src.domain.post.entities import Post
from src.domain.post.exc import PostException
from src.domain.post.services import IPostService
from src.infrastructure.dto.post import PostDto
from src.infrastructure.repositories.post import IPostRepository


@dataclass
class PostService(IPostService):
    repository: IPostRepository

    async def get_by_id(self, oid: str) -> Optional[Post]:
        dto = await self.repository.get_by_id(oid)
        if not dto:
            raise PostException("Post isn't found")
        return dto.to_entity()

    async def create(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.update(dto)
        if not dto:
            raise PostException("Post isn't found")
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
        search: Optional[str] = None,
    ) -> Optional[list[Post]]:
        post_iter = await self.repository.find_many(
            sort_field, sort_order, limit, offset, search
        )
        if not post_iter:
            raise PostException("Posts aren't found")
        return [post.to_entity() for post in post_iter]

    async def count_many(self, search: Optional[str] = None) -> int | None:
        count = await self.count_many(search)
        if not count:
            raise PostException("Posts aren't found")
        return count
