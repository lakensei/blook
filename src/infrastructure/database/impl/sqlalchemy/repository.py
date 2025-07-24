from typing import Any, Dict, List, Optional, Type, Tuple, Union, Set, TypeVar

from sqlalchemy import select, text, func, Executable, update, delete, inspect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.core.database.interfaces import CRUD, T, IdType
from src.common.core.database.repositories import Repository


class SQLAlchemyCRUD(CRUD[T]):
    """SQLAlchemy的CRUD实现"""
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model

    def _get_primary_key_columns(self) -> List:
        """
        获取模型的所有主键列
        """
        mapper = inspect(self.model)
        return list(mapper.primary_key)

    def _build_primary_key_condition(self, row_id: IdType) -> Union[Any, List[Any]]:
        """
        构建主键查询条件
        """
        primary_key_columns = self._get_primary_key_columns()

        if len(primary_key_columns) == 1:
            # 单主键
            if isinstance(row_id, dict):
                raise ValueError("单主键模型不应传入字典")
            return primary_key_columns[0] == row_id
        else:
            # 复合主键
            if not isinstance(row_id, dict):
                raise ValueError("复合主键模型需要传入字典")

            conditions = []
            for column in primary_key_columns:
                if column.name not in row_id:
                    raise ValueError(f"缺少复合主键字段: {column.name}")
                conditions.append(column == row_id[column.name])
            return conditions

    async def create(self, data: Dict) -> T:
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def get(self, row_id: IdType) -> Optional[T]:
        conditions = self._build_primary_key_condition(row_id)
        query = select(self.model).where(**conditions)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))
        return result.all()

    async def update(self, row_id: IdType, data: Dict) -> Optional[T]:
        try:
            # 验证ID是否存在
            existing_obj = await self.session.get(self.model, row_id)
            if not existing_obj:
                return None

            # 执行更新
            conditions = self._build_primary_key_condition(row_id)
            stmt = update(self.model).where(**conditions).values(**data)
            result = await self.session.execute(stmt)

            if result.rowcount > 0:
                await self.session.commit()
                # 刷新对象获取最新数据
                await self.session.refresh(existing_obj)
                return existing_obj
            else:
                await self.session.rollback()
                return None

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise Exception(f"数据库更新失败: {str(e)}")
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, row_id: IdType) -> bool:
        conditions = self._build_primary_key_condition(row_id)
        query = delete(self.model).where(**conditions)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    def field_filter(self, query: Executable, filters: Dict[str, Any]) -> Executable:
        """过滤器方法"""
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
        return query

    async def get_filtered(
            self,
            filters: Dict[str, Any],
            skip: int = 0,
            limit: int = 100,
            order_by: List[Tuple[str, bool]] = None,
            fields: Set[str] = None
    ) -> List[Dict]:
        # 构建查询字段
        if not fields:
            mapper = inspect(self.model)
            fields = [column.name for column in mapper.columns]

        columns = [getattr(self.model, field) for field in fields]
        query = select(*columns)

        # 处理过滤条件
        query = self.field_filter(query, filters)
        # 处理排序
        if order_by:
            for field, desc in order_by:
                column = getattr(self.model, field.lstrip('-'))
                query = query.order_by(column.desc() if desc else column.asc())

        query = query.offset(skip).limit(limit)
        print(query)
        result = await self.session.execute(query)
        instances = result.all()
        return [dict(zip(fields, row)) for row in instances]

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
            query = self.field_filter(query, filters)

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
