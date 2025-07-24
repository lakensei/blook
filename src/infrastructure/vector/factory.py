import logging
from typing import Optional, Type

from .base import BaseRegister
from .vector_registry import VectorRegistry

logger = logging.getLogger(__name__)


class VectorFactory:
    def __init__(self):
        self._impl_type: Optional[str] = None
        self._register: Optional[BaseRegister] = None

    def initialize(self, config: dict) -> None:
        """初始化数据库连接"""
        self._impl_type = config.get("impl_type")
        vector_class = VectorRegistry.get_register(self._impl_type)
        # 获取并执行初始化函数
        if not vector_class:
            raise ValueError(f"Unsupported Vector type: {self._impl_type}")
        self._register = vector_class(
            host=config["host"],
            port=config["port"]
        )
        self._register.connect(config["embedding_name"])
        logger.info(f"VectorFactory has been initialized")
