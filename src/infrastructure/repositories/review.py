from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterable, Optional

from pymongo import ReturnDocument

from src.infrastructure.db import Database
from src.infrastructure.dto.review import ReviewDto


@dataclass(frozen=True)
class IReviewRepository(ABC):
    database: Database
    collection_name: str = "review"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def get_by_oid(self, oid: str) -> Optional[ReviewDto]:
        pass

    @abstractmethod
    async def create(self, review: ReviewDto) -> ReviewDto:
        pass

    @abstractmethod
    async def update(self, review: ReviewDto) -> Optional[ReviewDto]:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass

    @abstractmethod
    async def find_many(
        self,
        post_id: str,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
    ) -> Optional[AsyncIterable[ReviewDto]]:
        pass

    @abstractmethod
    async def count_many(self, post_id: str) -> Optional[int]:
        pass


class MongoReviewRepository(IReviewRepository):
    async def get_by_oid(self, oid: str) -> Optional[ReviewDto]:
        doc = await self.collection.find_one({"oid": oid})
        return ReviewDto.load(doc)

    async def create(self, review: ReviewDto) -> ReviewDto:
        doc = await self.collection.insert_one(review.dump())
        doc = await self.collection.find_one({"_id": doc.inserted_id})
        return ReviewDto.load(doc)

    async def update(self, review: ReviewDto) -> Optional[ReviewDto]:
        doc = await self.collection.find_one_and_update(
            {"oid": review.oid},
            {"$set": review.dump()},
            return_document=ReturnDocument.AFTER,
        )
        return ReviewDto.load(doc)

    async def delete(self, oid: str) -> None:
        await self.collection.delete_one({"oid": oid})

    async def find_many(
        self,
        post_id: str,
        sort_field: str,
        sort_order: int,
        limit: int,
        offset: int,
    ) -> Optional[AsyncIterable[ReviewDto]]:
        cursor = (
            self.collection.find(post_id)
            .sort(sort_field, sort_order)
            .limit(limit)
            .skip(offset)
        )
        async for doc in cursor:
            yield ReviewDto.load(doc)

    async def count_many(self, post_id: str) -> Optional[int]:
        query = await self.collection.find(post_id)
        return await self.collection.count_documents(query)
