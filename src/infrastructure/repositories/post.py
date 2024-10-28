from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterable, Optional

from pymongo import ReturnDocument

from src.infrastructure.db import Database
from src.infrastructure.dto.post import PostDto


@dataclass(frozen=True)
class IPostRepository(ABC):
    database: Database
    collection_name: str = "post"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get_by_id(self, oid: str) -> Optional[PostDto]:
        pass

    @abstractmethod
    async def create(self, post: PostDto) -> PostDto:
        pass

    @abstractmethod
    async def update(self, post: PostDto) -> Optional[PostDto]:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass

    @abstractmethod
    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: Optional[str] = None,
    ) -> Optional[AsyncIterable[PostDto]]:
        pass

    @abstractmethod
    async def count_many(self, search: Optional[str] = None) -> Optional[int]:
        pass


class MongoPostRepository(IPostRepository):
    async def get_by_id(self, oid: str) -> Optional[PostDto]:
        doc = await self.collection.find_one({"oid": oid})
        return PostDto.load(doc)

    async def create(self, post: PostDto) -> PostDto:
        doc = await self.collection.insert_one(post.dump())
        doc = await self.collection.find_one({"oid": doc.oid})
        return PostDto.load(doc)

    async def update(self, post: PostDto) -> Optional[PostDto]:
        doc = await self.collection.find_one_and_update(
            {"oid": post.oid},
            {"$set": post.dump()},
            return_document=ReturnDocument.AFTER,
        )
        return PostDto.load(doc)

    async def delete(self, oid: str) -> None:
        await self.collection.delete_one({"oid": oid})

    def _build_find_query(search: Optional[str] = None):
        query = {}
        if search:
            search_query = {
                "$or": [{"title": {"regex": search}}, {"content": {"regex": search}}]
            }
            query.update(search_query)
        return query

    async def find_many(
        self,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
        search: Optional[str] = None,
    ) -> Optional[AsyncIterable[PostDto]]:
        query = self._build_find_query(search)
        cursor = (
            self.collection.find(query)
            .sort(sort_field, sort_order)
            .limit(limit)
            .skip(offset)
        )
        async for doc in cursor:
            yield PostDto.load(doc)

    async def count_many(self, search: Optional[str] = None) -> Optional[int]:
        query = self._build_find_query(search)
        return await self.collection.count_documents(query)
