import punq
from fastapi import APIRouter, Depends

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_auth.schemas import AuthorizeInSchema, AuthorizeOutSchema
from src.core.config.container import get_container
from src.domain.user_auth.commands import AuthorizeUserAuthCommand
from src.domain.user_auth.use_case import AuthorizeUseAuthUseCase

router = APIRouter()


@router.post("/authorize", response_model=ApiResponse[AuthorizeOutSchema])
async def authorize_user_auth_views(
    user_auth_in: AuthorizeInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[AuthorizeOutSchema]:
    command = AuthorizeUserAuthCommand(user=user_auth_in.to_entity())
    use_case: AuthorizeUseAuthUseCase = container.resolve(AuthorizeUseAuthUseCase)
    code = await use_case.execute(command)
    key = command.user.phone_number if command.user.phone_number else command.user.email
    return ApiResponse(
        data=AuthorizeOutSchema(
            msg=f"The code <{code}> has been sent to phone number or email <{key}>"
        )
    )
