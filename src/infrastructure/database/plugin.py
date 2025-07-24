import logging
from typing import Any, Dict

from .base import DatabasesConfig, PLUGIN_NAME
from .factory import DatabaseFactory
from ..base import InfrastructurePlugin

logger = logging.getLogger(__name__)


class DatabasePlugin(InfrastructurePlugin):
    """数据库插件"""
    name = PLUGIN_NAME

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._factory = DatabaseFactory()
        self._initialized: bool = False

    # def setup(self) -> None:
    #     """
    #     数据库插件初始化设置
    #     1. 加载ORM模块
    #     2. 注册数据库工厂到容器
    #     """
    #     if self._initialized:
    #         return
    #     # 调用父类setup注册服务和依赖
    #     super().setup()
    #     self._initialized = True

    # def get_lifespan(self, settings: Dict[str, Any]) -> AsyncGenerator:
    #     """
    #     数据库生命周期管理
    #     1. 初始化数据库连接
    #     2. 清理数据库连接
    #     """
    #
    #     @asynccontextmanager
    #     async def lifespan():
    #         try:
    #             # 初始化数据库连接
    #             self._factory.initialize(DatabasesConfig.from_settings(settings))
    #             logger.info("DatabasePlugin lifespan start")
    #             # actory = DatabaseFactory()
    #             # await factory.initialize(DatabasesConfig(**{**settings, **{'databases': {db_name: db_config}}}))
    #             # self._factories[db_name] = factory
    #
    #             # 注册依赖项到 InfrastructureContainer
    #             # dependency = create_repository_dependency(factory.get_repository_class(), factory.get_session)
    #             # InfrastructureContainer.register_dependency(db_name, dependency)
    #
    #             yield
    #         finally:
    #             # 清理数据库连接
    #             logger.info("DatabasePlugin lifespan off")
    #             await self._factory.cleanup()
    #
    #     return lifespan()

    def startup(self) -> None:
        self._factory.initialize(DatabasesConfig.from_settings(self.config))

    def get_provider(self) -> DatabaseFactory:
        """提供数据库工厂实例"""
        return self._factory

    # def get_dependencies(self) -> List[Any]:
    #     """获取数据库相关的依赖项"""
    #     return [
    #         get_db_session,
    #         get_repository
    #     ]

    async def cleanup(self) -> None:
        """清理数据库连接"""
        await self._factory.cleanup()

    @property
    def is_initialized(self) -> bool:
        """检查插件是否已初始化"""
        return self._initialized
