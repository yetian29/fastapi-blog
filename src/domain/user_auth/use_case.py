from dataclasses import dataclass

from src.domain.user_auth.commands import AuthorizeUserAuthCommand
from src.domain.user_auth.services import ICodeService, ISendService, IUserAuthService


@dataclass(frozen=True)
class AuthorizeUseAuthUseCase:
    code_service: ICodeService
    send_service: ISendService
    user_auth_service: IUserAuthService

    async def execute(self, command: AuthorizeUserAuthCommand) -> str:
        pass
