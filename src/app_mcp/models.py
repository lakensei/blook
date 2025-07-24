"""
MCP模型定义
"""

from sqlalchemy import Column, String, JSON, Integer, DateTime, func

from src.infrastructure.database.impl.sqlalchemy.base import BaseModel

class Mcp(BaseModel):
    __tablename__ = "deer_mcp"

    mcp_id = Column(String(50), primary_key=True)
    mcp_name = Column(String(50))
    mcp_desc = Column(String(50))
    mcp_type = Column(String(5), nullable=False)
    mcp_json = Column(JSON, nullable=False)
    creator = Column(String(50), nullable=False)
    status = Column(Integer, default=0)
    updater = Column(String(50), nullable=True)
    deleted = Column(Integer, default=0)
    create_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    update_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
