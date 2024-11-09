from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from src.domain.user_profile.entities import UserProfile


class UserProfileInSchema(BaseModel):
    user_name: str = ""
    date_of_birth: str = ""

    @field_validator("user_name")
    @classmethod
    def validate_user_name(cls, value: str = "") -> str:
        if not value:
            raise ValueError("Invalid user name. User name is required.")
        value = value.strip()
        if len(value) > 32:
            raise ValueError(
                "Invalid user name. User name has to be less than or equal 32 character."
            )
        return value

    @field_validator("date_of_birth")
    @classmethod
    def validate_date_of_birth(cls, value: str = "") -> str:
        if not value:
            raise ValueError("Invalid date of birth. Date of birth is required.")
        value = value.strip()
        if len(value) != 10:
            raise ValueError(
                "Invalid date of birth . Date of birth has to be equal 10 character."
            )
        return value

    def to_entity(self, **kwargs) -> UserProfile:
        return UserProfile(
            user_name=self.user_name, date_of_birth=self.date_of_birth, **kwargs
        )


class UserProfileOutSchema(BaseModel):
    oid: str
    user_name: str
    date_of_birth: str
    phone_number: Optional[str]
    email: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: UserProfile) -> "UserProfileOutSchema":
        return UserProfileOutSchema(
            oid=entity.oid,
            user_name=entity.user_name,
            date_of_birth=entity.date_of_birth,
            phone_number=entity.user.phone_number,
            email=entity.user.email,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
