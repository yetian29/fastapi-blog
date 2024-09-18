import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_profile.shemas import UserProfileInSchema, UserProfileOutSchema
from src.core.configs.containers import get_container
from src.domain.user_profile.commands import CreateOrUpdateUserProfileCommand
from src.domain.user_profile.use_cases import CreateOrUpdateUserProfileUseCase

router = APIRouter()


@router.post("/{user_id}", response_model=ApiResponse[UserProfileOutSchema])
async def create_or_update_user_profile_views(
    user_id: str,
    user_profile_in: UserProfileInSchema,
    phone_number: str = Header(),
    user_token: str = Header(),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserProfileOutSchema]:
    use_case: CreateOrUpdateUserProfileUseCase = container.resolve(CreateOrUpdateUserProfileUseCase)
    command = CreateOrUpdateUserProfileCommand(
        user_profile=user_profile_in.to_entity(
            user_id=user_id, phone_number=phone_number
        ),
    )
    user_profile = await use_case.execute(check=user_token, command=command)
    return ApiResponse(data=UserProfileOutSchema.from_entity(user_profile))
