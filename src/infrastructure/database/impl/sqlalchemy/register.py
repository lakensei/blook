import logging
from contextlib import asynccontextmanager
from typing import Dict, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession, async_sessionmaker

from ...base import DatabasesConfig, DatabaseConfig, BaseRegister

logger = logging.getLogger(__name__)


class SQLAlchemyRegister(BaseRegister):
    _session_factories: Dict[str, async_sessionmaker[AsyncSession]] = {}
    _engines: Dict[str, AsyncEngine] = {}

    @classmethod
    def initialize(cls, config: DatabasesConfig) -> None:
        """初始化SQLAlchemy"""
        logger.info("Initialize SQLAlchemy")
        cls._engines = {}
        cls._session_factories = {}
        for db_name, db_config in config.databases.items():
            engine = cls._create_engine(db_config)
            cls._engines[db_name] = engine
            # 创建session
            session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,

                autocommit=False,

                autoflush=False
            )
            cls._session_factories[db_name] = session_factory

    @classmethod
    async def cleanup(cls) -> None:
        """清理SQLAlchemy连接"""
        for engine in cls._engines.values():
            await engine.dispose()
        cls._engines.clear()
        cls._session_factories.clear()

    @classmethod
    def get_engine(cls, db_name: str) -> AsyncEngine:
        """获取数据库引擎"""
        if db_name not in cls._engines:
            raise ValueError(f"Database {db_name} not found")
        return cls._engines[db_name]

    # @classmethod
    # def get_session_factory(cls, db_name: str) -> dict[str, Callable[[], AsyncSession]]:
    #     """获取会话工厂"""
    #     if db_name not in cls._session_factories:
    #         raise ValueError(f"Database {db_name} not found")
    #     return cls._session_factories[db_name]

    # @classmethod
    # def get_session_dependency(cls, db_name: str) -> Callable[..., AsyncGenerator[AsyncSession, None]]:
    #     """获取会话依赖"""
    #
    #     async def session_dependency() -> AsyncGenerator[AsyncSession, None]:
    #         session = cls._session_factories[db_name]()
    #         try:
    #             yield session
    #         finally:
    #             await session.close()
    #
    #     return session_dependency

    @classmethod
    @asynccontextmanager
    async def get_session_dependency(cls, db_name: str = "default") -> AsyncGenerator[AsyncSession, None]:
        """获取会话依赖"""
        async with cls._session_factories[db_name]() as session:
            yield session

    @staticmethod
    def _create_engine(config: DatabaseConfig) -> AsyncEngine:
        """创建数据库引擎"""
        return create_async_engine(
            config.url,
            echo=config.echo,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            pool_pre_ping=config.pool_pre_ping
        )
