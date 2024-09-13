

from fastapi import APIRouter, Depends
import punq

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_auth.schemas import AuthorizeUserInSchema, AuthorizeUserOutSchema, LoginUserInSchema, LoginUserOutSchema
from src.core.configs.containers import get_container
from src.domain.user_auth.commands import AuthorizeUserCommand, LoginUserCommand
from src.domain.user_auth.use_cases import AuthorizeUserUseCase, LoginUserUseCase


router = APIRouter()

@router.post("/authorize", response_model=ApiResponse[AuthorizeUserOutSchema])
async def authorize_user_views(
    authorize_in: AuthorizeUserInSchema,
    container: punq.Container = Depends(get_container)
) -> ApiResponse[AuthorizeUserOutSchema]:
    use_case: AuthorizeUserUseCase = container.resolve(AuthorizeUserUseCase)
    command = AuthorizeUserCommand(
        authorize_in.to_entity()
    )
    code = await use_case.execute(command)
    return ApiResponse(
        data=AuthorizeUserOutSchema(
            msg=f"The code <{code}> has been sent to phone number: <{command.user.phone_number}>."
        )
    )

@router.post("/login", response_model=ApiResponse[LoginUserOutSchema])
async def authorize_user_views(
    login_in: LoginUserInSchema,
    container: punq.Container = Depends(get_container)
) -> ApiResponse[LoginUserOutSchema]:
    use_case: LoginUserUseCase = container.resolve(LoginUserUseCase)
    command = LoginUserCommand(phone_number=login_in.phone_number, code=login_in.code)
    token = await use_case.execute(command)
    return ApiResponse(
        data=LoginUserOutSchema(
            token=token
        )
    )