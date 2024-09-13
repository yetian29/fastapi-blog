from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.user_auth.entities import User
from src.infrastructure.dto.base import BaseDto


@dataclass
class UserDto(BaseDto):
    oid: str | None
    phone_number: str
    token: str
    created_at: datetime | None
    updated_at: datetime | None
    is_active: bool = False

    def __post_init__(self):
        if not self.oid:
            self.oid = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: dict | None) -> "UserDto":
        if not data:
            return None
        return UserDto(
            oid=data.get("oid"),
            phone_number=data.get("phone_number"),
            token=data.get("token"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            is_active=data.get("is_active"),
        )

    @staticmethod
    def from_entity(user: User) -> "UserDto":
        return UserDto(
            oid=user.oid,
            phone_number=user.phone_number,
            token=user.token,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
        )

    def to_entity(self) -> User:
        return User(
            oid=self.oid,
            phone_number=self.phone_number,
            token=self.token,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_active=self.is_active,
        )
