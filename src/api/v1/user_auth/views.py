import punq
from fastapi import APIRouter, Depends

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_auth.schemas import (
    AuthorizeInSchema,
    AuthorizeOutSchema,
    LoginInSchema,
    LoginOutSchema,
)
from src.core.config.container import get_container
from src.domain.user_auth.commands import AuthorizeUserAuthCommand, LoginUserAuthCommand
from src.domain.user_auth.use_case import AuthorizeUseAuthUseCase, LoginUserAuthUseCase

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


@router.post("/login", response_model=ApiResponse[LoginOutSchema])
async def login_user_auth_views(
    user_auth_in: LoginInSchema, container: punq.Container = Depends(get_container)
) -> ApiResponse[LoginOutSchema]:
    command = LoginUserAuthCommand(
        phone_number=user_auth_in.phone_number,
        email=user_auth_in.email,
        code=user_auth_in.code,
    )
    use_case: LoginUserAuthUseCase = container.resolve(LoginUserAuthUseCase)
    token = await use_case.execute(command)
    return ApiResponse(data=LoginOutSchema(token=token))
