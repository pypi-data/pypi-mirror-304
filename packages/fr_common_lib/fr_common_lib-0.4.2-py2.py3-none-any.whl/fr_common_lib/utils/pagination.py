from typing import Generic, TypeVar, List

from pydantic import BaseModel, Field

T = TypeVar("T")

class PageParams(BaseModel):
    offset: int = Field(0, ge=0, description="Number of items to skip")
    limit: int = Field(10, gt=0, le=1000,description="Maximum number of items to return")


class Slice(Generic[T], BaseModel):
    items: List[T]
    offset: int
    limit: int

    @classmethod
    def from_params(cls, items: List[T], params: PageParams) -> "Slice[T]":
        return cls(
            items=items,
            offset=params.offset,
            limit=params.limit,
        )