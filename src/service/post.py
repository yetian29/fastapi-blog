from dataclasses import dataclass
from typing import Optional

from src.domain.post.entities import Post
from src.domain.post.services import IPostService
from src.helper.exc import fail
from src.infrastructure.dto.post import PostDto
from src.infrastructure.repositories.post import IPostRepository
from src.service.exc import PostNotFoundException, PostsNotFoundException


@dataclass
class PostService(IPostService):
    repository: IPostRepository

    async def get_by_id(self, oid: str) -> Optional[Post]:
        dto = await self.repository.get_by_id(oid)
        if not dto:
            fail(PostNotFoundException)
        return dto.to_entity()

    async def create(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.create(dto)
        return dto.to_entity()

    async def update(self, post: Post) -> Post:
        dto = PostDto.from_entity(post)
        dto = await self.repository.update(dto)
        if not dto:
            fail(PostNotFoundException)
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
        post_iter = self.repository.find_many(
            sort_field, sort_order, limit, offset, search
        )
        if not post_iter:
            fail(PostsNotFoundException)
        return [post.to_entity() async for post in post_iter]

    async def count_many(self, search: Optional[str] = None) -> int | None:
        count = await self.repository.count_many(search)
        if not count:
            fail(PostsNotFoundException)
        return count
