from typing import Optional

import punq
from fastapi import APIRouter, Depends

from src.api.v1.post.schemas import PostInSchema, PostOutSchema
from src.api.v1.schemas import ApiResponse, ListPaginatedResponse, PaginationOutSchema
from src.core.config.container import get_container
from src.domain.post.command import (
    CreatePostCommand,
    DeletePostCommand,
    GetPostCommand,
    GetPostListCommand,
    UpdatePostCommand,
)
from src.domain.post.entities import PostSortFieldsEnum
from src.domain.post.use_case import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetPostListUseCase,
    GetPostUseCase,
    UpdatePostUseCase,
)
from src.domain.post.value_object import PaginationQuery, SortOrderEnum, SortQuery

router = APIRouter()


@router.post("", response_model=ApiResponse[PostOutSchema])
async def create_post_views(
    post_in: PostInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    command = CreatePostCommand(post=post_in.to_entity())
    use_case: CreatePostUseCase = container.resolve(CreatePostUseCase)
    post = await use_case.execute(command)
    return ApiResponse(data=PostOutSchema.from_entity(post))


@router.put("/{oid}", response_model=ApiResponse[PostOutSchema])
async def update_post_views(
    oid: str, post_in: PostInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    command = UpdatePostCommand(post=post_in.to_entity(oid))
    use_case: UpdatePostUseCase = container.resolve(UpdatePostUseCase)
    post = await use_case.execute(command)
    return ApiResponse(data=PostOutSchema.from_entity(post))


@router.delete("/{oid}", response_model=ApiResponse[PostOutSchema])
async def delete_post_views(
    oid: str, container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    command = DeletePostCommand(oid)
    use_case: DeletePostUseCase = container.resolve(DeletePostUseCase)
    post = await use_case.execute(command)
    return ApiResponse(data=PostOutSchema.from_entity(post))


@router.get("/{oid}", response_model=ApiResponse[PostOutSchema])
async def get_post_views(
    oid: str, container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    command = GetPostCommand(oid)
    use_case: GetPostUseCase = container.resolve(GetPostUseCase)
    post = await use_case.execute(command)
    return ApiResponse(data=PostOutSchema.from_entity(post))


def get_sort(
    sort_field: PostSortFieldsEnum = PostSortFieldsEnum.oid.value,
    sort_order: SortOrderEnum = SortOrderEnum.asc,
) -> SortQuery:  # type: ignore
    return SortQuery(sort_field, sort_order)


def get_pagination(page: int = 0, limit: int = 20) -> PaginationQuery:
    return PaginationQuery(page, limit)


def get_post_list_command_factory(
    search: Optional[str] = None,
    sort: SortQuery = Depends(get_sort),
    pagination: PaginationQuery = Depends(get_pagination),
) -> GetPostListCommand:
    return GetPostListCommand(search, sort, pagination)


@router.get("", response_model=ApiResponse[ListPaginatedResponse[PostOutSchema]])
async def find_many_views(
    command: GetPostListCommand = Depends(get_post_list_command_factory),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[ListPaginatedResponse[PostOutSchema]]:
    use_case: GetPostListUseCase = container.resolve(GetPostListUseCase)
    posts, count = await use_case.execute(command)
    return ApiResponse(
        data=ListPaginatedResponse(
            items=[PostOutSchema.from_entity(post) for post in posts],
            pagination=PaginationOutSchema(
                page=command.pagination.page,
                limit=command.pagination.limit,
                total=count,
            ),
        )
    )
