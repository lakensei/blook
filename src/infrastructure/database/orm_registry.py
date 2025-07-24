import logging
from typing import Dict, Type, Callable, AsyncGenerator, Any

from src.common.core.database.repositories import Repository
from .base import BaseRegister

logger = logging.getLogger(__name__)


class ORMRegistry:
    """ORM注册器"""
    # _session_getter = Dict[str, Callable] = {}
    _instance = None
    # register_class
    _repositories: Dict[str, Type[Repository]] = {}
    _register_class: Dict[str, Type[BaseRegister]] = {}

    # _initializers: Dict[str, Callable] = {}
    # _cleaners: Dict[str, Callable] = {}
    # _engine_getters: Dict[str, Callable] = {}
    # # _session_dependencies: Dict[str, Callable] = {}
    # _session_dependencies: Dict[str, Callable[..., AsyncGenerator[Any, None]]] = {}

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance

    @classmethod
    def register(
            cls,
            name: str,
            repository_class: Type[Repository],
            register_class
            # initializer: Callable,
            # cleaner: Callable,
            # engine_getter: Callable,
            # # session_getter: Callable,
            # session_dependency: Callable = None
    ) -> None:
        """注册ORM实现"""
        cls._repositories[name] = repository_class
        cls._register_class[name] = register_class
        # cls._initializers[name] = register_class.initialize
        # cls._cleaners[name] = register_class.cleanup
        # cls._engine_getters[name] = register_class.get_engine
        # # cls._session_getter[name] = session_getter
        # cls._session_dependencies[name] = register_class.get_session_dependency
        logger.info(f"register {name}")

    @classmethod
    def get_register(cls, name: str) -> Type[BaseRegister]:
        """获取注册类"""
        logger.info(f"get {name} register")
        return cls._register_class.get(name)

    @classmethod
    def get_repository(cls, name: str) -> Type[Repository]:
        """获取仓储类"""
        logger.info(f"get {name} repository")
        return cls._repositories.get(name)

    # @classmethod
    # def get_initializer(cls, name: str) -> Callable:
    #     """获取初始化函数"""
    #     return cls._register_class.get(name).initialize
    #
    # @classmethod
    # def get_cleaner(cls, name: str) -> Callable:
    #     """获取清理函数"""
    #     return cls._register_class.get(name).cleanup
    #
    # @classmethod
    # def get_engine(cls, name: str) -> Callable:
    #     """获取引擎获取函数"""
    #     return cls._register_class.get(name).get_engine
    #
    # @classmethod
    # def get_session_dependency(cls, name: str) -> Callable[..., AsyncGenerator[Any, None]]:
    #     """获取会话依赖"""
    #     return cls._register_class.get(name).get_session_dependency
