from typing import Any, Dict, Generic, List, TypeVar

from pydantic import BaseModel, Field

TData = TypeVar("TData")

TItems = TypeVar("TItems")


class PaginationOutSchema(BaseModel):
    page: int
    limit: int
    total: int


class ListPaginatedResponse(BaseModel, Generic[TItems]):
    items: List[TItems]
    pagination: PaginationOutSchema


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | List | Dict = Field(default_factory=Dict)
    meta: Dict[str, Any] = Field(default_factory=Dict)
    error: List[Any] = Field(default_factory=List)
