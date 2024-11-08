from dataclasses import dataclass

from src.domain.user_auth.commands import (
    AuthorizeUserAuthCommand,
    DeleteUserAuthCommand,
    GetUserAuthCommand,
    LoginUserAuthCommand,
)
from src.domain.user_auth.entities import UserAuth
from src.domain.user_auth.services import (
    ICodeService,
    ILoginService,
    ISendService,
    IUserAuthService,
)


@dataclass(frozen=True)
class AuthorizeUseAuthUseCase:
    code_service: ICodeService
    send_service: ISendService
    user_auth_service: IUserAuthService

    async def execute(self, command: AuthorizeUserAuthCommand) -> str:
        user = await self.user_auth_service.get_or_create(user=command.user)
        code = await self.code_service.generate_code(user)
        self.send_service.send_code(user, code)
        return code


@dataclass(frozen=True)
class LoginUserAuthUseCase:
    code_service: ICodeService
    login_service: ILoginService
    user_auth_service: IUserAuthService

    async def execute(self, command: LoginUserAuthCommand) -> str:
        user = await self.user_auth_service.get_by_phone_number_or_email(
            phone_number=command.phone_number, email=command.email
        )
        await self.code_service.validate_code(user=user, code=command.code)
        token = self.login_service.active_and_generate_token(user)
        await self.user_auth_service.update(user)
        return token


@dataclass(frozen=True)
class DeleteUserAuthUseCase:
    user_auth_service: IUserAuthService

    async def execute(self, command: DeleteUserAuthCommand) -> UserAuth:
        return await self.user_auth_service.delete(oid=command.oid)


@dataclass(frozen=True)
class GetUserAuthUseCase:
    user_auth_service: IUserAuthService

    async def execute(self, command: GetUserAuthCommand) -> UserAuth:
        return await self.user_auth_service.get_by_token(token=command.token)
