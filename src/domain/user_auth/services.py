from abc import ABC, abstractmethod
from typing import Optional

from src.domain.user_auth.entities import UserAuth


class ICodeService(ABC):
    @abstractmethod
    async def generate_code(self, user: UserAuth) -> str:
        pass

    @abstractmethod
    async def validate_code(self, user: UserAuth, code: str) -> None:
        pass


class ISendService(ABC):
    @abstractmethod
    def send_code(self, user: UserAuth, code: str) -> None:
        pass


class ILoginService(ABC):
    @abstractmethod
    def active_and_generate_token(self, user: UserAuth) -> str:
        pass


class IUserAuthService(ABC):
    @abstractmethod
    async def get_by_oid(self, oid: str) -> UserAuth:
        pass

    @abstractmethod
    async def get_by_phone_number_or_email(
        self, phone_number: Optional[str], email: Optional[str]
    ) -> UserAuth:
        pass

    @abstractmethod
    async def get_by_token(self, token: str) -> UserAuth:
        pass

    @abstractmethod
    async def get_or_create(self, user: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    async def create(self, user: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    async def update(self, user: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    async def delete(self, oid: str) -> UserAuth:
        pass
