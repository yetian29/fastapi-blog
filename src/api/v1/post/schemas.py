

from datetime import datetime
from pydantic import BaseModel

from src.domain.post.entities import Post


class PostInSchema(BaseModel):
    title: str
    description: str
    
    def to_entity(self) -> Post:
        return Post(        
            oid=None,
            title=self.title,
            description=self.description,
            created_at=None,
            updated_at=None
             )
        
class PostOutSchema(BaseModel):
    oid: str
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
    
    @staticmethod
    def from_entity(post: Post) -> "PostOutSchema":
        return PostOutSchema(
            oid=post.oid,
            title=post.title,
            description=post.description,
            created_at=post.created_at,
            updated_at=post.updated_at
        )
        