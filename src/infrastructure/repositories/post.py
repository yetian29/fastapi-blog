from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterable

from pymongo import ReturnDocument

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
    async def create(self, post: PostDto) -> PostDto:
        pass

    @abstractmethod
    async def update(self, post: PostDto) -> PostDto:
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
    async def create(self, post: PostDto) -> PostDto:
        try:
            new_post = await self.collection.insert_one(post.dump())
        except:
            fail(CreatePostNotSuccessException())
        else:
            created_post = await self.collection.find_one({"_id": new_post.inserted_id})
            return PostDto.load(created_post)

    async def update(self, post: PostDto) -> PostDto:
        try:
            updated_post = await self.collection.find_one_and_update(
                {"oid": post.oid}, 
                {"$set": post.dump()}, 
                return_document=ReturnDocument.AFTER

            )
        except:
            fail(UpdatePostNotSuccessException())
        else:
            return PostDto.load(updated_post)

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
            return PostDto.load(doc)

    def _build_find_query(self, search: str | None = None) -> dict:
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
        async for doc in cursor:
            yield PostDto.load(doc)

    async def count_many(self, search: str | None = None) -> int:
        query = self._build_find_query(search)
        return await self.collection.count_documents(query)
