from datetime import datetime

import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_profile.schemas import UserProfileInSchema, UserProfileOutSchema
from src.core.config.container import get_container
from src.domain.user_auth.commands import GetUserAuthCommand
from src.domain.user_auth.use_case import GetUserAuthUseCase
from src.domain.user_profile.commands import (
    CreateUserProfileCommand,
    GetUserProfileCommand,
    UpdateUserProfileCommand,
)
from src.domain.user_profile.use_case import (
    CreateUserProfileUseCase,
    GetUserProfileUseCase,
    UpdateUserProfileUseCase,
)

router = APIRouter()


@router.post("", response_model=ApiResponse[UserProfileOutSchema])
async def create_user_profile_views(
    user_profile_in: UserProfileInSchema,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)
    command2 = CreateUserProfileCommand(
        user_profile=user_profile_in.to_entity(user=user_auth)
    )
    use_case2: CreateUserProfileUseCase = container.resolve(CreateUserProfileUseCase)
    user_profile = await use_case2.execute(command2)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))


@router.put("/{oid}", response_model=ApiResponse[UserProfileOutSchema])
async def update_user_profile_views(
    oid: str,
    user_profile_in: UserProfileInSchema,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)

    command2 = GetUserProfileCommand(oid)
    use_case2: GetUserProfileUseCase = container.resolve(GetUserProfileUseCase)
    user_profile = await use_case2.execute(command2)

    command3 = UpdateUserProfileCommand(
        user_profile=user_profile_in.to_entity(
            oid=user_profile.oid,
            user=user_auth,
            created_at=user_profile.created_at,
            updated_at=datetime.now(),
        )
    )
    use_case3: UpdateUserProfileUseCase = container.resolve(UpdateUserProfileUseCase)
    updated_user_profile = await use_case3.execute(command3)
    return ApiResponse(data=UserProfileOutSchema.from_entity(updated_user_profile))


@router.get("/{oid}", response_model=ApiResponse[UserProfileOutSchema])
async def get_user_profile_views(
    oid: str,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    await use_case1.execute(command1)

    command2 = GetUserProfileCommand(oid)
    use_case2: GetUserProfileUseCase = container.resolve(GetUserProfileUseCase)
    user_profile = await use_case2.execute(command2)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))
