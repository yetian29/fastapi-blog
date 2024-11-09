from datetime import datetime

import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.review.schemas import ReviewInSchema, ReviewOutSchema
from src.api.v1.schemas import ApiResponse, ListPaginatedResponse, PaginationOutSchema
from src.core.config.container import get_container
from src.domain.base.commands import PaginationQuery, SortOrderEnum, SortQuery
from src.domain.review.commands import (
    CreateReviewCommand,
    DeleteReviewCommand,
    GetReviewCommand,
    GetReviewListCommand,
    UpdateReviewCommand,
)
from src.domain.review.entitties import ReviewSortFieldsEnum
from src.domain.review.use_case import (
    CreateReviewUseCase,
    DeleteReviewUseCase,
    GetReviewListUseCase,
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
    token: str = Header(alias="Auth-Token"),
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
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)

    command2 = GetReviewCommand(oid)
    use_case2: GetReviewUseCase = container.resolve(GetReviewUseCase)
    review = await use_case2.execute(command2)

    if user_auth.oid != review.author_id:
        raise ValueError("Invalid user.")

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


@router.delete("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def delete_review_views(
    oid: str,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ReviewOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)
    command2 = GetReviewCommand(oid)
    use_case: GetReviewUseCase = container.resolve(GetReviewUseCase)
    review = await use_case.execute(command2)
    if user_auth.oid != review.author_id:
        raise ValueError("Invalid user.")
    command3 = DeleteReviewCommand(oid)
    use_case3: DeleteReviewUseCase = container.resolve(DeleteReviewUseCase)
    deleted_review = await use_case3.execute(command3)
    return ApiResponse(data=ReviewOutSchema.from_entity(deleted_review))


@router.get("/{oid}", response_model=ApiResponse[ReviewOutSchema])
async def get_review_views(
    oid: str, container: punq.Container = Depends(get_container)
) -> ApiResponse[ReviewOutSchema]:
    command = GetReviewCommand(oid)
    use_case: GetReviewUseCase = container.resolve(GetReviewUseCase)
    review = await use_case.execute(command)
    return ApiResponse(data=ReviewOutSchema.from_entity(review))


def get_sort(
    sort_field: ReviewSortFieldsEnum = ReviewSortFieldsEnum.oid,  # type: ignore
    sort_order: SortOrderEnum = SortOrderEnum.asc,
) -> SortQuery:
    return SortQuery(sort_field.name, sort_order)


def get_pagination(page: int = 0, limit: int = 20) -> PaginationQuery:
    return PaginationQuery(page, limit)


def get_review_list_command_factory(
    post_id: str,
    sort: SortQuery = Depends(get_sort),
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetReviewListCommand:
    return GetReviewListCommand(post_id, sort, pagination)


@router.get("", response_model=ApiResponse[ListPaginatedResponse[ReviewOutSchema]])
async def get_review_list_views(
    command: GetReviewListCommand = Depends(get_review_list_command_factory),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[ReviewOutSchema]]:
    use_case: GetReviewListUseCase = container.resolve(GetReviewListUseCase)
    reviews, count = await use_case.execute(command)
    return ApiResponse(
        data=ListPaginatedResponse(
            items=[ReviewOutSchema.from_entity(review) for review in reviews],
            pagination=PaginationOutSchema(
                page=command.pagination.page,
                limit=command.pagination.limit,
                total=count,
            ),
        )
    )
