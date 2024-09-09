

from dataclasses import dataclass
from src.domain.post.commands import CreatePostCommand, DeletePostCommand, GetPostCommand, GetPostListCommand, UpdatePostCommand
from src.domain.post.entities import Post
from src.domain.post.services import IPostService
import asyncio


@dataclass
class CreatePostUseCase:
    services: IPostService
    
    async def execute(self, command: CreatePostCommand) -> Post:
        return await self.services.create(post=command.post)
        
@dataclass
class UpdatePostUseCase:
    services: IPostService
    
    async def execute(self, command: UpdatePostCommand) -> Post:
        return await self.services.create(post=command.post)

@dataclass
class DeletePostUseCase:
    services: IPostService
    
    async def execute(self, command: DeletePostCommand) -> Post:
        return await self.services.delete(oid=command.oid)

@dataclass
class GetPostUseCase:
    services: IPostService

    async def execute(self, command: GetPostCommand) -> Post:
        return await self.services.get_by_id(oid=command.oid)

@dataclass
class GetPostListUseCase:
    services: IPostService
    
    async def execute(self, command: GetPostListCommand) -> tuple[list[Post], int]:
        posts, count = await asyncio.gather(
            self.services.find_many(
                sort_field=command.sort.sort_field,
                sort_order=command.sort.sort_order,
                limit=command.pagination.limit,
                offset=command.pagination.offset,
                search=command.search
                
            ),
            self.services.count_many(
                search=command.search
            )
        )
        return posts, count