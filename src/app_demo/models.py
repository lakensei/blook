"""
MCP模型定义
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, JSON, Integer, DateTime, func, PrimaryKeyConstraint, SmallInteger, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.impl.sqlalchemy.base import Base


class Mcp(Base):
    __tablename__ = 'deer_mcp'
    __table_args__ = (
        PrimaryKeyConstraint('mcp_id', name='deer_mcp_pkey'),
    )

    mcp_id: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False, comment="MCP唯一标识")
    mcp_name: Mapped[str] = mapped_column(String(50), nullable=False, comment="MCP名称")
    mcp_desc: Mapped[str] = mapped_column(String(50), comment="MCP描述信息")
    mcp_type: Mapped[str] = mapped_column(String(5),comment="MCP类型:SSE")
    mcp_json: Mapped[dict] = mapped_column(JSONB, comment="MCP的JSON配置内容")
    creator: Mapped[str] = mapped_column(String(50), comment="创建人账号/ID")
    create_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=False, default=func.now(), comment="创建时间")
    status: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment="状态（0=停用，1=发布）")
    updater: Mapped[Optional[str]] = mapped_column(String(50))
    update_time: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=func.now())
    deleted: Mapped[Optional[int]] = mapped_column(SmallInteger, server_default=text('0'), comment="是否逻辑删除（0=正常，1=已删除）")

