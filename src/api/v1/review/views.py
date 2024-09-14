import punq
from fastapi import APIRouter, Depends

from src.api.v1.review.schemas import ReviewInSchema, ReviewOutSchema
from src.api.v1.schemas import ApiResponse
from src.core.configs.containers import get_container
from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    UpdateReviewCommand,
)
from src.domain.review.use_cases import (
    CreateReviewUseCase,
    DeleteReviewUseCase,
    UpdateReviewUseCase,
)

router = APIRouter()


@router.post("/", response_model=ApiResponse[ReviewOutSchema])
async def create_review_views(
    review_in: ReviewInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[ReviewOutSchema]:
    use_case: CreateReviewUseCase = container.resolve(CreateReviewUseCase)
    command = CreateReviewCommand(review=review_in.to_entity())
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))


@router.put("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def update_review_views(
    oid: str,
    review_in: ReviewInSchema,
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    use_case: UpdateReviewUseCase = container.resolve(UpdateReviewUseCase)
    command = UpdateReviewCommand(review=review_in.to_entity(oid=oid))
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))


@router.delete("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def delete_review_views(
    oid: str,
    review_in: ReviewInSchema,
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    use_case: DeleteReviewUseCase = container.resolve(DeleteReviewUseCase)
    command = DeleteReviewCommand(review=review_in.to_entity(oid=oid))
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))
