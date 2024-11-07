import re
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class AuthorizeInSchema(BaseModel):
    phone_number: Optional[str] = None
    email: Optional[str] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value: Optional[str] = None) -> Optional[str]:
        if not value:
            return None
        value = value.strip()
        if not value.isdigit():
            raise ValueError("Invalid phone number. The phone number must be numbers")
        elif len(value) != 10:
            raise ValueError("Invalid phone number. The phone number must be 10 number")
        return value

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str] = None) -> Optional[str]:
        if not value:
            return None
        value = value.strip()
        pattern = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError(
                "Invalid email format. Email must be the format 'example@example.com'."
            )
        return value

    @model_validator(mode="after")
    def check_phone_number_or_email(self) -> "AuthorizeInSchema":
        if not self.phone_number and not self.email:
            raise ValueError(
                "Invalid login. You must log in with phone number or email."
            )
        if self.phone_number and self.email:
            raise ValueError(
                "Invalid login. Not allowed to log in both phone number and email."
            )
        return self


class AuthorizeOutSchema(BaseModel):
    msg: str
