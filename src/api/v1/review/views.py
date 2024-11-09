from datetime import datetime

import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.review.schemas import ReviewInSchema, ReviewOutSchema
from src.api.v1.schemas import ApiResponse
from src.core.config.container import get_container
from src.domain.review.commands import (
    CreateReviewCommand,
    GetReviewCommand,
    UpdateReviewCommand,
)
from src.domain.review.use_case import (
    CreateReviewUseCase,
    GetReviewUseCase,
    UpdateReviewUseCase,
)
from src.domain.user_auth.commands import GetUserAuthCommand
from src.domain.user_auth.use_case import GetUserAuthUseCase

router = APIRouter()


@router.post("/{post_id}", response_model=ApiResponse[ReviewOutSchema])
async def create_review_views(
    post_id: str,
    review_in: ReviewInSchema,
    token: str = Header(alias="Auth-token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)

    command2 = CreateReviewCommand(
        review=review_in.to_entity(post_id=post_id, author_id=user_auth.oid)
    )
    use_case2: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    review = await use_case2.execute(command2)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))


@router.put("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def update_review_views(
    oid: str,
    review_in: ReviewInSchema,
    token: str = Header(alias="Auth-token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)

    command2 = GetReviewCommand(oid)
    use_case2: GetReviewUseCase = container.resolve(GetReviewUseCase)
    review = await use_case2.execute(command2)

    command3 = UpdateReviewCommand(
        review=review_in.to_entity(
            post_id=review.post_id,
            author_id=user_auth.oid,
            oid=oid,
            created_at=review.created_at,
            updated_at=datetime.now(),
        )
    )
    use_case3: UpdateReviewUseCase = container.resolve(UpdateReviewUseCase)
    updated_review = await use_case3.execute(command3)
    return ApiResponse(data=ReviewOutSchema.from_entity(updated_review))
