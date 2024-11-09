from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.user_auth.entities import UserAuth
from src.infrastructure.dto.base import BaseDto


@dataclass
class UserAuthDto(BaseDto):
    oid: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]
    token: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self) -> None:
        if not self.oid and not self.created_at and not self.updated_at:
            self.oid = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

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
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(entity: UserAuth) -> "UserAuthDto":
        return UserAuthDto(
            oid=entity.oid,
            phone_number=entity.phone_number,
            email=entity.email,
            token=entity.token,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> UserAuth:
        return UserAuth(
            oid=self.oid,
            phone_number=self.phone_number,
            email=self.email,
            token=self.token,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
