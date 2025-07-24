import logging
from typing import Any, Dict

from .base import PLUGIN_NAME, VectorsConfig
from .factory import VectorFactory
from ..base import InfrastructurePlugin
from ..loader import InfrastructureLoader


logger = logging.getLogger(__name__)


class VectorPlugin(InfrastructurePlugin):
    """数据库插件"""
    name = PLUGIN_NAME

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._factory = VectorFactory()
        self._loder: InfrastructureLoader = InfrastructureLoader()
        self._initialized: bool = False

    def connect(self):
        ...

    # def setup(self) -> None:
    #     """
    #     数据库插件初始化设置
    #     1. 加载ORM模块
    #     2. 注册数据库工厂到容器
    #     """
    #     if self._initialized:
    #         return
    #     # 加载ORM实现
    #     self._loder.load_all()
    #     # 调用父类setup注册服务和依赖
    #     super().setup()
    #     self._initialized = True

    def startup(self) -> None:
        self._factory.initialize(VectorsConfig.from_settings(self.config))

    def get_provider(self) -> VectorFactory:
        """提供数据库工厂实例"""
        return self._factory

    async def cleanup(self) -> None:
        """清理数据库连接"""
        await self._factory.cleanup()

    @property
    def is_initialized(self) -> bool:
        """检查插件是否已初始化"""
        return self._initialized
