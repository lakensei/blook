"""
MCP管理
"""
from fastapi import APIRouter

from .v1 import mcp_router as mcp_v1_router

mcp_router = APIRouter()
mcp_router.include_router(mcp_v1_router, prefix="/v1", tags=["v1"])

__all__ = ["mcp_router"]