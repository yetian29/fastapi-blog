from datetime import datetime

import punq
from fastapi import APIRouter, Depends, Header

from src.api.v1.schemas import ApiResponse
from src.api.v1.user_auth.schemas import (
    AuthorizeInSchema,
    AuthorizeOutSchema,
    LoginInSchema,
    LoginOutSchema,
    UserAuthInSchema,
    UserAuthOutSchema,
)
from src.core.config.container import get_container
from src.domain.user_auth.commands import (
    AuthorizeUserAuthCommand,
    DeleteUserAuthCommand,
    GetUserAuthCommand,
    LoginUserAuthCommand,
    UpdateUserAuthCommand,
)
from src.domain.user_auth.use_case import (
    AuthorizeUseAuthUseCase,
    DeleteUserAuthUseCase,
    GetUserAuthUseCase,
    LoginUserAuthUseCase,
    UpdateUserAuthUseCase,
)

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


@router.put("/{oid}", response_model=ApiResponse[UserAuthOutSchema])
async def update_user_auth_views(
    oid: str,
    user_auth_in: UserAuthInSchema,
    token: str = Header(alias="Auth-Token"),
    container: punq.Container = Depends(get_container),
) -> ApiResponse[UserAuthOutSchema]:
    command1 = GetUserAuthCommand(token)
    use_case1: GetUserAuthUseCase = container.resolve(GetUserAuthUseCase)
    user_auth = await use_case1.execute(command1)
    if user_auth.phone_number:
        if (
            user_auth_in.phone_number
            and user_auth_in.phone_number != user_auth.phone_number
        ):
            raise ValueError(
                "Invalid phone number. Phone number isn't allowed changing."
            )
        user_auth.email = user_auth_in.email if user_auth_in.email else user_auth.email
    else:
        if user_auth_in.email and user_auth_in.email != user_auth.email:
            raise ValueError("Invalid email. Email isn't allowed changing.")
        user_auth.phone_number = (
            user_auth_in.phone_number
            if user_auth_in.phone_number
            else user_auth.phone_number
        )

    command2 = UpdateUserAuthCommand(
        user=user_auth_in.to_entity(
            oid=oid,
            phone_number=user_auth.phone_number,
            email=user_auth.email,
            is_active=user_auth.is_active,
            created_at=user_auth.created_at,
            updated_at=datetime.now(),
        )
    )
    use_case2: UpdateUserAuthUseCase = container.resolve(UpdateUserAuthUseCase)
    await use_case2.execute(command2)


@router.delete("/{oid}", response_model=ApiResponse[UserAuthOutSchema])
async def delete_user_auth_views(
    oid: str, container: punq.Container = Depends(get_container)
) -> ApiResponse[UserAuthOutSchema]:
    command = DeleteUserAuthCommand(oid)
    use_case: DeleteUserAuthUseCase = container.resolve(DeleteUserAuthUseCase)
    user_auth = await use_case.execute(command)
    return ApiResponse(data=UserAuthOutSchema.from_entity(user_auth))
