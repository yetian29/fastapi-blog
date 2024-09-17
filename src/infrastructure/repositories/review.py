from abc import ABC, abstractmethod
from dataclasses import dataclass

from pymongo import ReturnDocument

from src.domain.review.errors import (
    CreateReviewNotSuccessException,
    ReviewNotFoundException,
    UpdateReviewNotSuccessException,
)
from src.helper.errors import fail
from src.infrastructure.database import Database
from src.infrastructure.dto.review import ReviewDto


@dataclass
class IReviewRepository(ABC):
    database: Database
    collection_name: str = "reviews"

    @property
    def collection(self):
        return self.database.connection.get_collection(self.collection_name)

    @abstractmethod
    async def create(self, review: ReviewDto) -> ReviewDto:
        pass

    @abstractmethod
    async def update(self, review: ReviewDto) -> ReviewDto:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, oid: str) -> ReviewDto:
        pass

    @abstractmethod
    async def get_by_user_id_and_post_id(
        self, user_id: str, post_id: str
    ) -> ReviewDto:
        pass


class MongoReviewRepository(IReviewRepository):
    async def create(self, review: ReviewDto) -> ReviewDto:
        try:
            new_review = await self.collection.insert_one(review.dump())
        except:
            fail(CreateReviewNotSuccessException())
        else:
            created_review = await self.collection.find_one(
                {"_id": new_review.inserted_id}
            )
            return ReviewDto.load(created_review)

    async def update(self, review: ReviewDto) -> ReviewDto:
        try:
            updated_review = await self.collection.find_one_and_update(
                {"oid": review.oid},
                {"$set": review.dump()},
                return_document=ReturnDocument.AFTER,
            )
        except:
            fail(UpdateReviewNotSuccessException())
        else:
            return ReviewDto.load(updated_review)

    async def delete(self, oid: str) -> None:
        await self.collection.delete_one({"oid": oid})

    async def get_by_id(self, oid: str) -> ReviewDto:
        try:
            doc = await self.collection.find_one({"oid": oid})
        except:
            fail(ReviewNotFoundException())
        else:
            return ReviewDto.load(doc)

    async def get_by_user_id_and_post_id(
        self, user_id: str, post_id: str
    ) -> ReviewDto:
        try:
            doc = await self.collection.find_one(
                {"user_id": user_id, "post_id": post_id}
            )
        except:
            fail(ReviewNotFoundException())
        else:
            return ReviewDto.load(doc)
