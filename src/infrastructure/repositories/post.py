from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterable

from src.domain.post.errors import (
    CreatePostNotSuccessException,
    DeletePostNotSuccessException,
    PostNotFoundException,
    UpdatePostNotSuccessException,
)
from src.helper.errors import fail
from src.infrastructure.database import Database
from src.infrastructure.dto.post import PostDto


@dataclass
class IPostRepository(ABC):
    database: Database
    collection_name: str = "posts"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def create(self, post: PostDto) -> None:
        pass

    @abstractmethod
    async def update(self, post: PostDto) -> None:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, oid: str) -> PostDto:
        pass

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> AsyncIterable[PostDto]:
        pass

    @abstractmethod
    async def count_many(self, search: str | None = None) -> int:
        pass


class MongoPostRepository(IPostRepository):
    async def create(self, post: PostDto) -> None:
        try:
            await self.collection.insert_one({"post": post.dump()})
        except:
            fail(CreatePostNotSuccessException())

    async def update(self, post: PostDto) -> None:
        try:
            await self.collection.find_one_and_update(
                {"oid": post.oid}, {"$set": post.dump()}
            )
        except:
            fail(UpdatePostNotSuccessException())

    async def delete(self, oid: str) -> None:
        try:
            await self.collection.delete_one({"oid": oid})
        except:
            fail(DeletePostNotSuccessException())

    async def get_by_id(self, oid: str) -> PostDto:
        try:
            doc = await self.collection.find_one({"oid": oid})
        except:
            fail(PostNotFoundException())
        else:
            PostDto.load(doc)

    def _build_find_query(search: str | None = None):
        query = {}
        if search:
            search_query = {
                "$or": [
                    {"name": {"$regex": search}},
                    {"description": {"$regex": search}},
                ]
            }
            query.update(search_query)
        return query

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: str | None = None,
    ) -> AsyncIterable[PostDto]:
        query = self._build_find_query(search)
        cursor = (
            self.collection.find(query)
            .sort(sort_field, sort_order)
            .skip(offset)
            .limit(limit)
        )
        for doc in cursor:
            yield PostDto.load(doc)

    async def count_many(self, search: str | None = None) -> int:
        query = self._build_find_query(search)
        return await self.collection.count_documents(query)
