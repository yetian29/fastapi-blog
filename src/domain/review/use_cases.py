from dataclasses import dataclass

from src.domain.post.services import IPostService
from src.domain.review.commands import (
    CreateOrUpdateReviewCommand,
    DeleteReviewCommand,
)
from src.domain.review.entities import Review
from src.domain.review.services import IReviewService
from src.domain.user_auth.errors import UserInvalidException
from src.domain.user_auth.services import IUserService
from src.helper.errors import fail


@dataclass
class CreateOrUpdateReviewUseCase:
    review_service: IReviewService
    user_service: IUserService
    post_service: IPostService

    async def execute(self, command: CreateOrUpdateReviewCommand) -> Review:
        user = await self.user_service.get_by_id(oid=command.review.user_id)
        if user.token == command.user_token: 
            await self.post_service.get_by_id(oid=command.review.post_id)
            return await self.review_service.create_or_update(review=command.review)
        else:
            fail(UserInvalidException())


@dataclass
class DeleteReviewUseCase:
    review_service: IReviewService

    async def execute(self, command: DeleteReviewCommand) -> Review:
        return await self.review_service.delete(oid=command.oid)
