import logging
from abc import ABC, abstractmethod
from typing import Any, Dict

from pydantic import BaseModel

from .container import InfrastructureContainer
from .loader import InfrastructureLoader

logger = logging.getLogger(__name__)


class BaseConfig(BaseModel):
    impl_type: str


class InfrastructurePlugin(ABC):
    """基础设施插件基类"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        # self._dependencies: List[Any] = []
        self._loder: InfrastructureLoader = InfrastructureLoader()
        self._initialized: bool = False

    @property
    @abstractmethod
    def name(self) -> str:
        """插件名称"""
        pass

    def setup(self) -> None:
        """
        插件初始化设置，在插件加载时调用
        用于：
        1. 加载必要的模块
        2. 注册依赖项
        3. 初始化插件状态
        4. 注册服务到容器
        """
        if self._initialized:
            return
        # 加载ORM实现
        self._loder.load(self.config["IMPL_TYPE"])
        # 注册插件提供的服务到容器
        provider = self.get_provider()
        if provider:
            InfrastructureContainer.register_service(self.name, provider)

        # # 注册插件的依赖项
        # try:
        #     dependencies = self.get_dependencies()
        #     if dependencies:
        #         self._dependencies.extend(dependencies)
        #         for dependency in dependencies:
        #             InfrastructureContainer.register_dependency(
        #                 f"{self.name}_{dependency.__name__}",
        #                 dependency
        #             )
        # except Exception as e:
        #     logger.error(f"Error registering dependencies for plugin {self.name}: {str(e)}")
        #     raise

        self._initialized = True

    # @abstractmethod
    # def get_lifespan(self, settings: Dict[str, Any]) -> AsyncGenerator:
    #     """
    #     获取插件的生命周期管理器
    #     用于：
    #     1. 初始化资源连接
    #     2. 启动必要的服务
    #     3. 清理资源
    #     """
    #     pass

    @abstractmethod
    def startup(self) -> None:
        pass

    def get_provider(self) -> Any:
        """
        获取插件提供的服务
        用于：
        1. 提供给其他模块使用的服务实例
        2. 如数据库工厂、缓存客户端等
        """
        return None

    # def get_dependencies(self) -> List[Any]:
    #     """
    #     获取插件的依赖项
    #     用于：
    #     1. 注册FastAPI依赖项
    #     2. 提供依赖注入支持
    #     """
    #     return []

    async def cleanup(self) -> None:
        """
        清理插件资源
        """
        pass

    # @property
    # def dependencies(self) -> List[Any]:
    #     """获取已注册的依赖项"""
    #     return self._dependencies

    @property
    def is_initialized(self) -> bool:
        """检查插件是否已初始化"""
        return self._initialized
