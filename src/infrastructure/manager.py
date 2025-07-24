import logging
from contextlib import asynccontextmanager
from typing import Dict, Type, Optional, Callable, Any, Generator

from fastapi import FastAPI

from .base import InfrastructurePlugin
from .container import InfrastructureContainer
from .database.plugin import DatabasePlugin
from .vector.plugin import VectorPlugin

logger = logging.getLogger(__name__)


class InfrastructureManager:
    _available_plugins: Dict[str, Type[InfrastructurePlugin]] = {
        "database": DatabasePlugin,
        "vector": VectorPlugin,
        # "redis": RedisPlugin,
        # "celery": CeleryPlugin
    }

    def __init__(self):
        self._plugins: Dict[str, InfrastructurePlugin] = {}

    @classmethod
    def get_plugin_class(cls, name: str) -> Optional[Type[InfrastructurePlugin]]:
        """获取插件类"""
        return cls._available_plugins.get(name)

    def register_plugin(self, plugin_class: Type[InfrastructurePlugin], plugin_config: Dict[str, Any]) -> None:
        """注册插件"""
        # if init_on_startup:
        #     # 在服务启动时初始化
        #     plugin = plugin_class(plugin_config)
        # else:
        #     # 按需初始化
        #     plugin = (plugin_class, plugin_config)
        plugin = plugin_class(plugin_config)
        self._plugins[plugin.name] = plugin
        logger.info(f"Registered plugin: {plugin.name}")

    def load_plugins(self) -> Callable[[FastAPI], Generator[Any, Any, Any] | Any]:
        """加载所有插件"""

        # 创建插件生命周期管理器
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            # 初始化所有插件
            for plugin in self._plugins.values():
                logger.info(f"Setting up plugin: {plugin.name}")
                try:
                    # 调用插件初始化设置
                    plugin.setup()
                    # 注册插件到容器
                    InfrastructureContainer.register_plugin(plugin.name, plugin)
                    # 插件启动
                    plugin.startup()
                    logger.info(f"Plugin {plugin.name} initialized successfully")
                except Exception as e:
                    logger.error(f"Failed to initialize plugin {plugin.name}: {str(e)}")
                    raise

            yield

            # 清理工作
            logger.info("Starting cleanup of plugins...")
            for plugin_name in reversed(list(self._plugins.keys())):
                try:
                    logger.debug(f"Cleaning up plugin: {plugin_name}")
                    await self._plugins[plugin_name].cleanup()
                    logger.info(f"Plugin {plugin_name} cleaned up successfully")
                except Exception as e:
                    logger.error(f"Error cleaning up plugin {plugin_name}: {str(e)}")
            InfrastructureContainer.clear()
        # 设置应用的生命周期管理器
        # app.router.lifespan_context = lifespan
        logger.info("Set the application lifecycle manager")
        return lifespan

    @classmethod
    def register_available_plugin(cls, name: str, plugin_class: Type[InfrastructurePlugin]) -> None:
        """注册可用插件类"""
        cls._available_plugins[name] = plugin_class
        logger.info(f"Added new available plugin: {name}")
