from datetime import datetime
from typing import Optional

import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.post.schemas import PostInSchema, PostOutSchema
from src.api.v1.schemas import ApiResponse, ListPaginatedResponse, PaginationOutSchema
from src.core.config.container import get_container
from src.domain.base.commands import SortOrderEnum
from src.domain.post.command import (
    CreatePostCommand,
    DeletePostCommand,
    GetPostCommand,
    GetPostListCommand,
    PaginationQuery,
    SortQuery,
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
from src.domain.user_auth.commands import GetUserAuthCommand
from src.domain.user_auth.use_case import GetUserAuthUseCase

router = APIRouter()


@router.post("", response_model=ApiResponse[PostOutSchema])
async def create_post_views(
    post_in: PostInSchema,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[PostOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)
    command2 = CreatePostCommand(post=post_in.to_entity(author_id=user_auth.oid))
    use_case2: CreatePostUseCase = container.resolve(CreatePostUseCase)
    post = await use_case2.execute(command2)
    return ApiResponse(data=PostOutSchema.from_entity(post))


@router.put("/{oid}", response_model=ApiResponse[PostOutSchema])
async def update_post_views(
    oid: str,
    post_in: PostInSchema,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[PostOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)

    command2 = GetPostCommand(oid)
    use_case2: GetPostUseCase = container.resolve(GetPostUseCase)
    post = await use_case2.execute(command2)
    if user_auth.oid != post.author_id:
        raise ValueError("Invalid user.")
    command3 = UpdatePostCommand(
        post=post_in.to_entity(
            oid=oid,
            author_id=user_auth.oid,
            created_at=post.created_at,
            updated_at=datetime.now(),
        )
    )
    use_case3: UpdatePostUseCase = container.resolve(UpdatePostUseCase)
    updated_post = await use_case3.execute(command3)
    return ApiResponse(data=PostOutSchema.from_entity(updated_post))


@router.delete("/{oid}", response_model=ApiResponse[PostOutSchema])
async def delete_post_views(
    oid: str,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[PostOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)
    command2 = GetPostCommand(oid)
    use_case2: GetPostUseCase = container.resolve(GetPostUseCase)
    post = await use_case2.execute(command2)
    if user_auth.oid != post.author_id:
        raise ValueError("Invalid user.")
    command3 = DeletePostCommand(oid)
    use_case3: DeletePostUseCase = container.resolve(DeletePostUseCase)
    deleted_post = await use_case3.execute(command3)
    return ApiResponse(data=PostOutSchema.from_entity(deleted_post))


@router.get("/{oid}", response_model=ApiResponse[PostOutSchema])
async def get_post_views(
    oid: str, container: punq.Container = Depends(get_container)
) -> ApiResponse[PostOutSchema]:
    command = GetPostCommand(oid)
    use_case: GetPostUseCase = container.resolve(GetPostUseCase)
    post = await use_case.execute(command)
    return ApiResponse(data=PostOutSchema.from_entity(post))


def get_sort(
    sort_field: PostSortFieldsEnum = PostSortFieldsEnum.oid,  # type: ignore
    sort_order: SortOrderEnum = SortOrderEnum.asc,
) -> SortQuery:
    return SortQuery(sort_field.name, sort_order)


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
