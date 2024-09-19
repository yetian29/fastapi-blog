import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_profile.shemas import UserProfileInSchema, UserProfileOutSchema
from src.core.configs.containers import get_container
from src.domain.user_profile.commands import CreateUserProfileCommand, GetUserProfileCommand
from src.domain.user_profile.use_cases import CreateUserProfileUseCase, GetUserProfileUseCase

router = APIRouter()


@router.post("/{user_id}", response_model=ApiResponse[UserProfileOutSchema])
async def create_user_profile_views(
    user_id: str,
    user_profile_in: UserProfileInSchema,
    phone_number: str = Header(),
    user_token: str = Header(),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    use_case: CreateUserProfileUseCase = container.resolve(
        CreateUserProfileUseCase
    )
    command = CreateUserProfileCommand(
        user_profile=user_profile_in.to_entity(
            user_id=user_id, phone_number=phone_number
        ),
    )
    user_profile = await use_case.execute(check=user_token, command=command)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))

@router.put("/{user_id}/{oid}", response_model=ApiResponse[UserProfileOutSchema])
async def update_user_profile_views(
    oid: str,
    user_id: str,
    user_profile_in: UserProfileInSchema,
    phone_number: str = Header(),
    user_token: str = Header(),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    use_case: CreateUserProfileUseCase = container.resolve(
        CreateUserProfileUseCase
    )
    command = CreateUserProfileCommand(
        user_profile=user_profile_in.to_entity(
            oid=oid,
            user_id=user_id,
            phone_number=phone_number
        ),
    )
    user_profile = await use_case.execute(user_token=user_token, user_id=user_id, command=command)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))


@router.get("/{user_id}/{oid}", response_model=ApiResponse[UserProfileOutSchema])
async def update_user_profile_views(
    oid: str,
    user_id: str,
    user_profile_in: UserProfileInSchema,
    phone_number: str = Header(),
    user_token: str = Header(),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    use_case: GetUserProfileUseCase = container.resolve(
        GetUserProfileUseCase
    )
    command = GetUserProfileCommand(
        user_profile=user_profile_in.to_entity(
            oid=oid,
            user_id=user_id,
            phone_number=phone_number
        ),
    )
    user_profile = await use_case.execute(user_token=user_token, user_id=user_id, command=command)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))
