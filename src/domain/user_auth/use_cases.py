

from dataclasses import dataclass
from src.domain.user_auth.commands import AuthorizeUserCommand, LoginUserCommand
from src.domain.user_auth.services import ICodeService, ILoginService, ISendService, IUserService

@dataclass
class AuthorizeUserUseCase:
    code_service: ICodeService
    send_service: ISendService
    user_service: IUserService
    
    async def execute(self, command: AuthorizeUserCommand) -> str:
        user = await self.user_service.get_or_create(user=command.user)
        code = await self.code_service.generate_code(phone_number=user.phone_number)
        await self.send_service.send_code(phone_number=user.phone_number, code=code)
        return code
        

@dataclass
class LoginUserUseCase:
    code_service: ICodeService
    login_service: ILoginService
    user_service: IUserService
    
    async def execute(self, command: LoginUserCommand) -> str:
        user = await self.user_service.get(phone_number=command.phone_number)
        await self.code_service.validate_code(phone_number=user.phone_number, code=command.code)
        return await self.login_service.activate_and_generate_token(user)
             