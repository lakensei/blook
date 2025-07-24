from typing import TypeVar, List, Generic

from pydantic import BaseModel

Item = TypeVar("Item")


class PaginatedRes(BaseModel, Generic[Item]):
    data: List[Item]
    total: int
    page: int
    page_size: int
    total_pages: int