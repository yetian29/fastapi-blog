from datetime import datetime

from pydantic import BaseModel

from src.domain.user_profile.entities import UserProfile


class UserProfileInSchema(BaseModel):
    username: str
    date_of_birth: str

    def to_entity(self, user_id: str, phone_number: str) -> UserProfile:
        return UserProfile(
            oid=None,
            user_id=user_id,
            phone_number=phone_number,
            username=self.username,
            date_of_birth=self.date_of_birth,
            created_at=None,
            updated_at=None,
        )


class UserProfileOutSchema(BaseModel):
    oid: str
    user_id: str
    phone_number: str
    username: str
    date_of_birth: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(user: UserProfile) -> "UserProfileOutSchema":
        return UserProfileOutSchema(
            oid=user.oid,
            user_id=user.user_id,
            phone_number=user.phone_number,
            username=user.username,
            date_of_birth=user.date_of_birth,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
