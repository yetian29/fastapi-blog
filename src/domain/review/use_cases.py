from dataclasses import dataclass

from src.domain.post.services import IPostService
from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    GetReviewCommand,
    UpdateReviewCommand,
)
from src.domain.review.entities import Review
from src.domain.review.services import IReviewService
from src.domain.user_auth.errors import UserInvalidException
from src.domain.user_auth.services import IUserService
from src.helper.errors import fail


@dataclass
class CreateReviewUseCase:
    review_service: IReviewService
    user_service: IUserService
    post_service: IPostService

    async def execute(self, user_token, user_id: str, post_id: str, command: CreateReviewCommand) -> Review:
        user = await self.user_service.get_by_id(oid=user_id)
        if user.token == user_token:
            await self.post_service.get_by_id(oid=post_id)
            return await self.review_service.create(review=command.review)
        else:
            fail(UserInvalidException())


@dataclass
class UpdateReviewUseCase:
    review_service: IReviewService
    user_service: IUserService
    post_service: IPostService

    async def execute(self, user_token: str, user_id: str, post_id: str, command: UpdateReviewCommand) -> Review:
        user = await self.user_service.get_by_id(oid=user_id)
        if user.token == user_token:
            await self.post_service.get_by_id(oid=post_id)
            return await self.review_service.update(review=command.review)
        else:
            fail(UserInvalidException())


@dataclass
class DeleteReviewUseCase:
    review_service: IReviewService
    user_service: IUserService


    async def execute(self, user_token: str, user_id: str, command: DeleteReviewCommand) -> Review:
        user = await self.user_service.get_by_id(oid=user_id)
        if user.token == user_token:
            return await self.review_service.delete(oid=command.oid)
        else:
            fail(UserInvalidException())


@dataclass
class GetReviewUseCase:
    review_service: IReviewService
    user_service: IUserService

    async def execute(self, user_token: str, user_id: str, command: GetReviewCommand) -> Review:
        user = await self.user_service.get_by_id(oid=user_id)
        if user.token == user_token:
            return await self.review_service.get_by_id(oid=command.oid)
        else:
            fail(UserInvalidException())
