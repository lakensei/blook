from typing import List, Tuple, Type, Dict, Any, Set

from src.common.core.database.interfaces import CRUD
from src.common.core.response import PaginatedRes, T


def compute_offset(page: int, page_size: int) -> int:
    return (page - 1) * page_size

def compute_total_page(total_count: int, page_size: int) -> int:
    return (total_count + page_size - 1) // page_size if page_size > 0 else 1

async def paginate(
    crud: CRUD[T],
    filters: Dict[str, Any] = {"deleted": 0},
    page: int = 1,
    page_size: int = 100,
    order_by: List[Tuple[str, bool]] = [("create_time", False)],
    fields: Set[str] = None
) -> PaginatedRes[Dict]:
    """
    处理分页查询
    :param crud: CRUD 实例
    :param filters: 过滤条件
    :param page: 当前页数（从 1 开始）
    :param page_size: 每页条数
    :param order_by: 排序条件
    :param fields: 指定查询字段
    :return: 分页响应
    """
    # 计算 skip
    skip = compute_offset(page, page_size)

    # 获取数据和总数
    total_count = await crud.count(filters)
    if total_count == 0:
        return PaginatedRes[T](
            page=page,
            page_size=page_size
        )
    items = await crud.get_filtered(filters, skip, page_size, order_by, fields)


    return PaginatedRes[Dict](
        data=items,
        total=total_count,
        page=page,
        page_size=page_size,
        total_pages=compute_total_page(total_count, page_size)
    )