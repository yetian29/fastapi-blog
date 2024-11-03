from typing import Optional

from src.domain.user_auth.entities import UserAuth
from src.infrastructure.dto.base import BaseDto


class UserAuthDto(BaseDto):
    oid: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    token: str
    is_active: bool

    @staticmethod
    def load(data: Optional[dict]) -> "UserAuthDto":
        if not data:
            return None
        return UserAuthDto(
            oid=data.get("oid"),
            phone_number=data.get("phone_number"),
            email=data.get("email"),
            token=data.get("token"),
            is_active=data.get("is_active"),
        )

    @staticmethod
    def from_entity(entity: UserAuth) -> "UserAuthDto":
        return UserAuthDto(
            oid=entity.oid,
            phone_number=entity.phone_number,
            email=entity.email,
            token=entity.tokne,
            is_active=entity.is_active,
        )

    def to_entity(self) -> UserAuth:
        return UserAuth(
            oid=self.oid,
            phone_number=self.phone_number,
            email=self.email,
            token=self.token,
            is_active=self.is_active,
        )
