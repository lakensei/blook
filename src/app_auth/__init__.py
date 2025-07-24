"""
认证
"""
from fastapi import APIRouter

from .v1 import auth_router as auth_v1_router

auth_router = APIRouter()
auth_router.include_router(auth_v1_router, prefix="/v1/auth", tags=["v1"])

__all__ = ["auth_router"]
