from abc import ABC, abstractmethod

from src.domain.user_auth.entities import UserAuth


class ICodeService(ABC):
    @abstractmethod
    def generate_code(self, user: UserAuth) -> str:
        pass

    @abstractmethod
    def validate_code(self, user: UserAuth, code: str) -> None:
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
    def get_or_create(self, user: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    def update(self, user: UserAuth) -> UserAuth:
        pass

    @abstractmethod
    def delete(self, oid: str) -> UserAuth:
        pass
