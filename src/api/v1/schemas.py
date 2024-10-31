from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

TData = TypeVar("TData")

TItems = TypeVar("TItems")


class PaginationOutSchema(BaseModel):
    page: int
    limit: int
    total: int


class ListPaginatedResponse(BaseModel, Generic[TItems]):
    items: list[TItems]
    pagination: PaginationOutSchema


class ApiResponse(BaseModel, Generic[TData]):
    data: TData | list | dict = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)
    error: list[Any] = Field(default_factory=list)
