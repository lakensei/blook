import logging
from importlib import import_module
from typing import Dict

logger = logging.getLogger(__name__)


class InfrastructureLoader:

    _modules: Dict[str, str] = {
        "sqlalchemy": "src.infrastructure.database.impl.sqlalchemy",
        "milvus": "src.infrastructure.vector.impl.milvus",
        # "tortoise": "src.infrastructure.database.impl.tortoise.register"
    }

    @classmethod
    def register(cls, name: str, module_path: str) -> None:
        """注册新的插件"""
        cls._modules[name] = module_path

    @classmethod
    def load(cls, name: str) -> None:
        """加载指定的插件"""
        if name not in cls._modules:
            raise ValueError(f"Unknown plugin: {name}")
        module = import_module(cls._modules[name])
        register_handle = getattr(module, "init_register")
        register_handle()
        logger.info(f"load plugin {name}")

    # @classmethod
    # def load_all(cls) -> None:
    #     """加载所有已注册的插件"""
    #     for name in cls._modules:
    #         cls.load(name)
