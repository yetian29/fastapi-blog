import re
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator

from src.domain.user_auth.entities import UserAuth


class BaseValidate(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str] = None) -> Optional[str]:
        if not value:
            return None
        elif not value.isdigit():
            raise ValueError("Invalid phone number. The phone number must be numbers")
        elif len(value) != 10:
            raise ValueError("Invalid phone number. The phone number must be 10 number")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str] = None) -> Optional[str]:
        if not value:
            return None
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Invalid email format. Email must be the format 'example@gmail.com'."
            )
        return value

    @model_validator(mode="after")
    def check_phone_number_or_email(self) -> "AuthorizeInSchema":
        if not self.phone_number and not self.email:
            raise ValueError(
                "Invalid login. You must log in with phone number or email."
            )
        elif self.phone_number and self.email:
            raise ValueError(
                "Invalid login. Not allowed to log in both phone number and email."
            )
        return self


class AuthorizeInSchema(BaseValidate):
    def to_entity(self) -> UserAuth:
        return UserAuth(phone_number=self.phone_number, email=self.email)


class AuthorizeOutSchema(BaseModel):
    msg: str


class LoginInSchema(BaseValidate):
    code: str


class LoginOutSchema(BaseModel):
    token: str
