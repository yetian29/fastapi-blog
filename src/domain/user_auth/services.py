from abc import ABC, abstractmethod

from src.domain.user_auth.entities import User


class ICodeService(ABC):
    @abstractmethod
    async def generate_code(self, phone_number: str) -> str:
        pass

    @abstractmethod
    async def validate_code(self, phone_number: str, code: str) -> None:
        pass


class ISendService(ABC):
    @abstractmethod
    async def send_code(self, phone_number: str, code: str) -> None:
        pass


class ILoginService(ABC):
    @abstractmethod
    async def activate_and_generate_token(self, user: User) -> str:
        pass


class IUserService(ABC):
    @abstractmethod
    async def get_or_create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, oid: str) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass
