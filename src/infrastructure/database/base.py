from contextlib import asynccontextmanager
from typing import Dict, Any, TypeVar

from pydantic import BaseModel

from ..base import BaseConfig


class DatabaseConfig(BaseModel):
    url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_pre_ping: bool = True


class DatabasesConfig(BaseConfig):
    databases: Dict[str, DatabaseConfig]

    @classmethod
    def from_settings(cls, settings: Dict[str, Any]) -> "DatabasesConfig":
        # databases = {}
        # for db_type, urls in settings.items():
        #     if db_type != "IMPL_TYPE":
        #         databases[db_type] = {
        #             name: DatabaseConfig(url=url)
        #             for name, url in urls.items()
        #         }

        return cls(
            impl_type=settings["IMPL_TYPE"],
            databases={
                name: DatabaseConfig(url=url)
                for name, url in settings["DATABASE_URLS"].items()
            }
        )


AsyncSession = TypeVar("AsyncSession")
AsyncEngine = TypeVar("AsyncEngine")


class BaseRegister:
    @classmethod
    def initialize(cls, config: DatabasesConfig) -> None:
        raise NotImplementedError

    @classmethod
    async def cleanup(cls) -> None:
        raise NotImplementedError

    @classmethod
    def get_engine(cls, db_name: str) -> AsyncEngine:
        raise NotImplementedError

    @classmethod
    @asynccontextmanager
    async def get_session_dependency(cls, db_name: str) -> AsyncSession:
        raise NotImplementedError


PLUGIN_NAME: str = "database"
