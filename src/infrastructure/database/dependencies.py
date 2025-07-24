from typing import AsyncGenerator, Any

from .base import PLUGIN_NAME
from .factory import DatabaseFactory
from ..container import InfrastructureContainer


def get_db_factory() -> DatabaseFactory:
    """获取数据库工厂依赖"""
    factory = InfrastructureContainer.get_service(PLUGIN_NAME)
    if not factory:
        raise RuntimeError("Database factory not initialized")
    return factory


async def get_db_session(db_name: str = "default") -> AsyncGenerator[Any, None]:
    """默认数据库会话依赖"""
    factory = get_db_factory()
    async with factory.get_session(db_name) as session:
        yield session


async def get_repository(db_name: str = "default") -> AsyncGenerator[Any, None]:
    """获取数据库curd"""
    factory = get_db_factory()
    repository_class = factory.get_repository_class()
    async with factory.get_session(db_name) as session:
        yield repository_class(session)
