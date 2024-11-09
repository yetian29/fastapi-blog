import asyncio
from dataclasses import dataclass

from src.domain.post.command import (
    CreatePostCommand,
    DeletePostCommand,
    GetPostCommand,
    GetPostListCommand,
    UpdatePostCommand,
)
from src.domain.post.entities import Post
from src.domain.post.services import IPostService


@dataclass(frozen=True)
class CreatePostUseCase:
    service: IPostService

    async def execute(self, command: CreatePostCommand) -> Post:
        return await self.service.create(post=command.post)


@dataclass(frozen=True)
class UpdatePostUseCase:
    service: IPostService

    async def execute(self, command: UpdatePostCommand) -> Post:
        return await self.service.update(post=command.post)


@dataclass(frozen=True)
class DeletePostUseCase:
    service: IPostService

    async def execute(self, command: DeletePostCommand) -> Post:
        return await self.service.delete(oid=command.oid)


@dataclass(frozen=True)
class GetPostUseCase:
    service: IPostService

    async def execute(self, command: GetPostCommand) -> Post:
        return await self.service.get_by_oid(oid=command.oid)


@dataclass(frozen=True)
class GetPostListUseCase:
    service: IPostService

    async def execute(self, command: GetPostListCommand) -> tuple[list[Post], int]:
        return await asyncio.gather(
            self.service.find_many(
                sort_field=command.sort.sort_field,
                sort_order=command.sort.sort_order,
                limit=command.pagination.limit,
                offset=command.pagination.offset,
                search=command.search,
            ),
            self.service.count_many(search=command.search),
        )
