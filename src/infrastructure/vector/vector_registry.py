import logging
from typing import Dict, Type

from .base import BaseRegister

logger = logging.getLogger(__name__)


class VectorRegistry:
    """注册器"""
    _instance = None
    _register_class: Dict[str, Type[BaseRegister]] = {}

    @classmethod
    def register(
            cls,
            name: str,
            register_class

    ) -> None:
        cls._register_class[name] = register_class
        logger.info(f"register {name}")

    @classmethod
    def get_register(cls, name: str) -> Type[BaseRegister]:
        """获取注册类"""
        logger.info(f"get {name} register")
        return cls._register_class.get(name)
