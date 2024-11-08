import punq
from fastapi import APIRouter, Depends

from src.api.v1.review.schemas import ReviewInSchema, ReviewOutSchema
from src.api.v1.schemas import ApiResponse
from src.core.config.container import get_container
from src.domain.review.commands import CreateReviewCommand
from src.domain.review.use_case import CreateReviewUseCase

router = APIRouter()


@router.post("/{post_id}", response_model=ApiResponse[ReviewOutSchema])
async def create_review_views(
    review_in: ReviewInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[ReviewOutSchema]:
    command = CreateReviewCommand(review=review_in.to_entity())
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))
