from abc import ABC, abstractmethod
from typing import Generic, Type

from .interfaces import CRUD, T


class Repository(ABC, Generic[T]):
    """仓储接口"""

    @abstractmethod
    def get_crud(self, model: Type[T]) -> CRUD[T]:
        """获取CRUD操作接口"""
        pass
