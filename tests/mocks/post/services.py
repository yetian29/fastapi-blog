

from datetime import datetime
import random
from uuid import uuid4
from src.domain.post.entities import Post
from src.domain.post.services import IPostService
from tests.mocks.post.factories import PostFactory


class DummyPostService(IPostService):
    
    async def create(self, post: Post) -> Post:
        post.oid = str(uuid4())
        post.created_at = datetime.now()
        post.updated_at = datetime.now()
        return post
    
    async def update(self, post: Post) -> Post:
        return post
    
    async def delete(self, oid: str) -> Post:
        return PostFactory.build(oid)
    
    async def get_by_id(self, oid: str) -> Post:
        return PostFactory.build(oid)
    
    async def find_many(
        self, sort_field: str, 
        sort_order: int, 
        limit: int, offset: int, 
        search: str | None = None
        ) -> list[Post]:
        return [PostFactory.build() for _ in range(random.randint(0, limit))]
    
    async def count_many(self, search: str | None = None) -> int:
        return random.randint(0, 1000)  