import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class InfrastructureContainer:
    """基础设施容器，用于管理插件、服务和依赖项"""

    _plugins: Dict[str, Any] = {}
    _services: Dict[str, Any] = {}
    # _dependencies: Dict[str, Any] = {}

    @classmethod
    def register_plugin(cls, name: str, plugin: Any) -> None:
        """注册插件实例"""
        cls._plugins[name] = plugin
        logger.info(f"Registered plugin in container: {plugin.__class__.__name__}")

    @classmethod
    def register_service(cls, name: str, service: Any) -> None:
        """注册服务实例"""
        cls._services[name] = service
        logger.info(f"Registered service in container: {service.__class__.__name__}")
        logger.debug(f"container service: {service.__dict__}")
    #
    # @classmethod
    # def register_dependency(cls, name: str, dependency: Any) -> None:
    #     """注册依赖项"""
    #     cls._dependencies[name] = dependency

    @classmethod
    def get_plugin(cls, name: str) -> Optional[Any]:
        """获取插件实例"""
        logger.info(f"get plugin from container: {cls._plugins.get(name).__dict__}")
        return cls._plugins.get(name)

    @classmethod
    def get_service(cls, name: str) -> Optional[Any]:
        """获取服务实例"""
        logger.info(f"get service from container: {name}")
        return cls._services.get(name)
    #
    # @classmethod
    # def get_dependency(cls, name: str) -> Optional[Any]:
    #     """获取依赖项"""
    #     return cls._dependencies.get(name)

    @classmethod
    def clear(cls) -> None:
        """清理容器"""
        cls._plugins.clear()
        cls._services.clear()
        logger.info(f"clear container")
        # cls._dependencies.clear()
