from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field


TData = TypeVar("TData")
TItem = TypeVar("TItem")


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | list | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    errors: list[Any] = Field(default_factory=list)



class PaginationOutSchema(BaseModel):
    page: int
    limit: int
    total: int
    
    
class ListPaginatedResponse(BaseModel, Generic[TItem]):
    items: list[TItem]
    pagination: PaginationOutSchema