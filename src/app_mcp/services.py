from typing import List, Dict, Any

from sqlalchemy import select, desc

from src.app_mcp.models import Mcp
from src.infrastructure.database.base import AsyncSession


class McpService:

    @staticmethod
    async def save(db: AsyncSession, item: Mcp):
        stmt = select(Mcp).where(Mcp.mcp_id == item.mcp_id)
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()

        if existing:
            existing.mcp_name = item.mcp_name
            existing.mcp_desc = item.mcp_desc
            existing.mcp_json = item.mcp_json
            existing.updater = item.creator
            existing.deleted = item.deleted
            existing.status = item.status
        else:
            db.add(item)

    @staticmethod
    async def get_by_id(db: AsyncSession, mcp_id: str) -> List[dict]:
        stmt = select(Mcp.mcp_id, Mcp.mcp_name, Mcp.mcp_desc, Mcp.mcp_json).where(Mcp.mcp_id == mcp_id)
        result = await db.execute(stmt)
        data = result.scalar_one_or_none()
        return data

    @staticmethod
    async def get_page_list(
            db: AsyncSession,
            page: int = 1,
            page_size: int = 10
    ) -> Dict[str, Any]:
        """
        分页
        :param db: AsyncSession 实例
        :param page: 当前页码（从 1 开始）
        :param page_size: 每页数量
        :return: 包含分页结果和总数的字典
        """
        # 构建查询语句
        stmt = (
            select(Mcp.mcp_id, Mcp.mcp_name, Mcp.mcp_desc, Mcp.mcp_json,
                   Mcp.creator, Mcp.create_time)
            .where(Mcp.deleted == 0)
            .order_by(desc(Mcp.create_time))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        count_stmt = (
            select(Mcp.mcp_id)
            .where(Mcp.deleted == 0)
        )
        result = await db.execute(stmt)
        paginated_results = [
            dict(zip(result.keys(), row)) for row in result.all()
        ]
        total_result = await db.execute(count_stmt)
        total = len(total_result.all())
        return {
            "data": paginated_results,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size
        }
