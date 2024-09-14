import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.review.schemas import ReviewInSchema, ReviewOutSchema
from src.api.v1.schemas import ApiResponse
from src.core.configs.containers import get_container
from src.domain.review.commands import (
    CreateOrUpdateReviewCommand,
    DeleteReviewCommand,
)
from src.domain.review.use_cases import (
    CreateOrUpdateReviewUseCase,
    DeleteReviewUseCase,
)

router = APIRouter()


@router.post("/{post_id}", response_model=ApiResponse[ReviewOutSchema])
async def create_or_update_review_views(
    post_id: str,
    review_in: ReviewInSchema,
    user_token: str = Header(),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    use_case: CreateOrUpdateReviewUseCase = container.resolve(
        CreateOrUpdateReviewUseCase
    )
    command = CreateOrUpdateReviewCommand(
        review=review_in.to_entity(user_token=user_token, post_id=post_id)
    )
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))


@router.delete("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def delete_review_views(
    oid: str,
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    use_case: DeleteReviewUseCase = container.resolve(DeleteReviewUseCase)
    command = DeleteReviewCommand(oid=oid)
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))
