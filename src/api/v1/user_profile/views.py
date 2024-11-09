import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_profile.schemas import UserProfileInSchema, UserProfileOutSchema
from src.core.config.container import get_container
from src.domain.user_auth.commands import GetUserAuthCommand
from src.domain.user_auth.use_case import GetUserAuthUseCase
from src.domain.user_profile.commands import CreateUserProfileCommand
from src.domain.user_profile.use_case import CreateUserProfileUseCase

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
