

from pydantic import BaseModel

from src.domain.user_auth.entities import User


class AuthorizeUserInSchema(BaseModel):
    phone_number: str
    
    def to_entity(self) -> User:
        return User(
            oid=None,
            phone_number=self.phone_number,
            token=None,
            is_active=False,
            created_at=None, 
            updated_at=None          
        )
    

class AuthorizeUserOutSchema(BaseModel):
    msg: str

class LoginUserInSchema(BaseModel):
    phone_number: str
    code: str


class LoginUserOutSchema(BaseModel):
    token: str