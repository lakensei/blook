from typing import Any, Dict, List, Optional, Type, Tuple, Union, Set

from sqlalchemy import select, text, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.core.database.interfaces import CRUD, T
from src.common.core.database.repositories import Repository


class SQLAlchemyCRUD(CRUD[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    async def create(self, data: Dict) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get(self, id: Any) -> Optional[T]:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_filtered(
            self,
            filters: Dict[str, Any],
            skip: int = 0,
            limit: int = 100,
            order_by: List[Tuple[str, bool]] = None,
            fields: Set[str] = None
    ) -> List[T]:
        # 构建查询字段
        if fields:
            columns = [getattr(self.model, field) for field in fields]
            query = select(*columns)
        else:
            query = select(self.model)

        # 处理过滤条件
        for key, value in filters.items():
            if '__' in key:
                field, op = key.split('__')
                if op == 'gte':
                    query = query.where(getattr(self.model, field) >= value)
                elif op == 'lte':
                    query = query.where(getattr(self.model, field) <= value)
                elif op == 'in':
                    query = query.where(getattr(self.model, field).in_(value))
                elif op == 'like':
                    query = query.where(getattr(self.model, field).like(f'%{value}%'))
                elif op == 'isnull':
                    if value:
                        query = query.where(getattr(self.model, field).is_(None))
                    else:
                        query = query.where(getattr(self.model, field).isnot(None))
            else:
                query = query.where(getattr(self.model, key) == value)

        # 处理排序
        if order_by:
            for field, desc in order_by:
                column = getattr(self.model, field.lstrip('-'))
                if desc:
                    query = query.order_by(column.desc())
                else:
                    query = query.order_by(column)

        query = query.offset(skip).limit(limit)
        result = await self.session.execute(query)

        if fields:
            # 如果指定了字段，返回字典列表
            return [dict(zip(fields, row)) for row in result.fetchall()]
        return result.scalars().all()

    async def execute_query(
            self,
            query: str,
            params: Dict[str, Any] = None,
            as_model: bool = True
    ) -> Union[List[T], List[Dict[str, Any]]]:
        stmt = text(query)
        result = await self.session.execute(stmt, params or {})

        if as_model:
            # 尝试将结果映射到模型
            return [self.model(**dict(row)) for row in result.mappings()]
        else:
            # 返回字典列表
            return [dict(row) for row in result.mappings()]

    async def count(self, filters: Dict[str, Any] = None) -> int:
        query = select(func.count()).select_from(self.model)

        if filters:
            for key, value in filters.items():
                if '__' in key:
                    field, op = key.split('__')
                    if op == 'gte':
                        query = query.where(getattr(self.model, field) >= value)
                    elif op == 'lte':
                        query = query.where(getattr(self.model, field) <= value)
                else:
                    query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one()

    async def exists(self, filters: Dict[str, Any]) -> bool:
        count = await self.count(filters)
        return count > 0


class SQLAlchemyRepository(Repository[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    def get_crud(self, model: Type[T]) -> CRUD[T]:
        return SQLAlchemyCRUD(self.session, model)
