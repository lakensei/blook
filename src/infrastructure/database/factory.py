import logging
from contextlib import asynccontextmanager
from typing import Optional, Type, AsyncGenerator

from src.common.core.database.repositories import Repository
from .base import DatabasesConfig, AsyncSession, AsyncEngine, BaseRegister
from .orm_registry import ORMRegistry

logger = logging.getLogger(__name__)


class DatabaseFactory:
    def __init__(self):
        self._impl_type: Optional[str] = None
        self._register: Optional[Type[BaseRegister]] = None
        self._repository_class: Optional[Type[Repository]] = None

    def initialize(self, config: DatabasesConfig) -> None:
        """初始化数据库连接"""
        self._impl_type = config.impl_type
        self._register = ORMRegistry.get_register(self._impl_type)
        self._repository_class = ORMRegistry.get_repository(self._impl_type)
        # 获取并执行初始化函数
        initializer = self._register.initialize
        if not initializer:
            raise ValueError(f"Unsupported ORM type: {self._impl_type}")
        initializer(config)
        logger.info(f"DatabaseFactory has been initialized")

    @asynccontextmanager
    async def get_session(
            self,
            db_name: str = "default"
    ) -> AsyncGenerator[AsyncSession, None]:
        """获取数据库会话"""
        if not self._impl_type:
            raise RuntimeError("DatabaseFactory not initialized")
        session_getter = self._register.get_session_dependency
        if not session_getter:
            raise ValueError(f"No session found for ORM type: {self._impl_type}")
        # yield session_getter(db_name)
        async with session_getter(db_name) as session:
            yield session

    async def cleanup(self) -> None:
        """清理数据库连接"""
        cleaner = self._register.cleanup
        if cleaner:
            await cleaner()
            logger.info(f"cleaner {cleaner.__name__}")

    def get_engine(self, db_name: str) -> AsyncEngine:
        """获取指定的数据库引擎"""
        engine_getter = self._register.get_engine(self._impl_type)
        if not engine_getter:
            raise ValueError(f"No engine found for ORM type: {self._impl_type}")
        return engine_getter(db_name)

    @property
    def impl_type(self) -> str:
        if not self._impl_type:
            raise RuntimeError("DatabaseFactory not initialized")
        return self._impl_type

    def get_repository_class(self) -> Type[Repository]:
        if not self._impl_type:
            raise RuntimeError("DatabaseFactory not initialized")
        if not self._repository_class:
            raise ValueError(f"No repository found for ORM type: {self._impl_type}")
        return self._repository_class
