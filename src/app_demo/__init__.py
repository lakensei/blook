"""
MCP管理示例
"""
from fastapi import APIRouter

from .v1 import demo_router as demo_v1_router

demo_router = APIRouter()
demo_router.include_router(demo_v1_router, prefix="/v1", tags=["v1"])

__all__ = ["demo_router"]