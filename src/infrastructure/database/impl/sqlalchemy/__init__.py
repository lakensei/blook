from .base import BaseModel, Base
from .register import SQLAlchemyRegister
from .repository import SQLAlchemyRepository

from ...orm_registry import ORMRegistry


def init_register():
    # 注册SQLAlchemy
    ORMRegistry.register(
        "sqlalchemy",
        SQLAlchemyRepository,
        SQLAlchemyRegister
        # SQLAlchemyRegister.initialize,
        # SQLAlchemyRegister.cleanup,
        # SQLAlchemyRegister.get_engine,
        # SQLAlchemyRegister.get_session_dependency
        # # get_sqlalchemy_session
    )


__all__ = [
    "init_register",
    "BaseModel",
    "Base",
]
