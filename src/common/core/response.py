from typing import TypeVar, List, Generic

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class PaginatedRes(BaseModel, Generic[T]):
    data: List[T] = []
    total: int = 0
    page: int
    page_size: int
    total_pages: int = 0