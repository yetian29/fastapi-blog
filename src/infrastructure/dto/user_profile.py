from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from src.domain.user_profile.entities import UserProfile
from src.infrastructure.dto.base import BaseDto


@dataclass
class UserProfileDto(BaseDto):
    oid: str | None
    user_id: str
    phone_number: str
    username: str
    date_of_birth: str
    created_at: datetime | None
    updated_at: datetime | None

    def __post_init__(self):
        if not self.oid:
            self.oid = str(uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()

    @staticmethod
    def load(data: dict | None) -> "UserProfileDto":
        if not data:
            return None
        return UserProfileDto(
            oid=data.get("oid"),
            user_id=data.get("user_id"),
            phone_number=data.get("phone_number"),
            username=data.get("username"),
            date_of_birth=data.get("date_of_birth"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    @staticmethod
    def from_entity(user: UserProfile) -> "UserProfileDto":
        return UserProfileDto(
            oid=user.oid,
            user_id=user.user_id,
            phone_number=user.phone_number,
            username=user.username,
            date_of_birth=user.date_of_birth,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def to_entity(self) -> UserProfile:
        return UserProfile(
            oid=self.oid,
            user_id=self.user_id,
            phone_number=self.phone_number,
            username=self.username,
            date_of_birth=self.date_of_birth,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
