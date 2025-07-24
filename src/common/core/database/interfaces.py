from abc import ABC, abstractmethod
from typing import Any, Dict, List, AsyncGenerator, Optional, TypeVar, Tuple, Union, Set
from typing import Generic

T = TypeVar('T')
IdType = Union[int, str, Dict[str, Any]]

class Database(ABC):
    """数据库接口"""

    @abstractmethod
    async def connect(self) -> None:
        """连接数据库"""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """断开数据库连接"""
        pass

    @abstractmethod
    async def get_session(self) -> AsyncGenerator[Any, None]:
        """获取数据库会话"""
        pass


class CRUD(ABC, Generic[T]):
    """CRUD操作接口"""

    @abstractmethod
    async def create(self, data: Dict) -> T:
        pass

    @abstractmethod
    async def get(self, row_id: IdType) -> Optional[T]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        pass

    @abstractmethod
    async def update(self, row_id: IdType, data: Dict) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, row_id: IdType) -> bool:
        pass

    @abstractmethod
    async def get_filtered(
            self,
            filters: Dict[str, Any],
            skip: int = 0,
            limit: int = 100,
            order_by: List[Tuple[str, bool]] = None,
            fields: Set[str] = None  # 指定返回的字段
    ) -> List[Dict]:
        """
        获取过滤后的结果
        :param filters: 过滤条件，如 {"status": "active", "age__gte": 18}
        :param skip: 跳过记录数
        :param limit: 返回记录数
        :param order_by: 排序条件列表，如 [("created_at", True)] True表示降序
        :param fields: 需要返回的字段集合，如 {"id", "name", "email"}
        """
        pass

    @abstractmethod
    async def execute_query(
            self,
            query: str,
            params: Dict[str, Any] = None,
            as_model: bool = True
    ) -> Union[List[T], List[Dict[str, Any]]]:
        """
        执行原生SQL查询
        :param query: SQL查询语句
        :param params: 查询参数
        :param as_model: 是否返回模型实例，False则返回字典
        :return: 查询结果列表
        """
        pass

    @abstractmethod
    async def count(self, filters: Dict[str, Any] = None) -> int:
        """
        获取记录数量
        :param filters: 过滤条件
        :return: 记录数量
        """
        pass

    @abstractmethod
    async def exists(self, filters: Dict[str, Any]) -> bool:
        """
        检查记录是否存在
        :param filters: 过滤条件
        :return: 是否存在
        """
        pass
