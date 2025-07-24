from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, DateTime, String, SmallInteger, text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class BaseModel(Base):
    """SQLAlchemy基础模型"""
    __abstract__ = True

    creator: Mapped[str] = mapped_column(String(50), comment="创建人账号/ID")
    create_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    status: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment="状态（0=停用，1=发布）")
    updater: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
    deleted: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment="是否逻辑删除（0=正常，1=已删除）")
