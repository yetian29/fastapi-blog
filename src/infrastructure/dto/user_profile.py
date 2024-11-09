from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import uuid4

from src.domain.user_auth.entities import UserAuth
from src.domain.user_profile.entities import UserProfile
from src.infrastructure.dto.base import BaseDto


@dataclass
class UserProfileDto(BaseDto):
    oid: str
    user_name: str
    date_of_birth: str
    user: UserAuth
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if not self.oid and not self.created_at and not self.updated_at:
            self.oid = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: Optional[dict]) -> "UserProfileDto":
        if not data:
            return None
        return UserProfileDto(
            oid=data.get("oid"),
            user_name=data.get("user_name"),
            date_of_birth=data.get("date_of_birth"),
            user=data.get("user"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(entity: UserProfile) -> "UserProfileDto":
        return UserProfileDto(
            oid=entity.oid,
            user_name=entity.user_name,
            date_of_birth=entity.date_of_birth,
            user=entity.user,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_entity(self) -> UserProfile:
        return UserProfile(
            oid=self.oid,
            user_name=self.user_name,
            date_of_birth=self.date_of_birth,
            user=self.user,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
