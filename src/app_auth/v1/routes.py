from fastapi import APIRouter, Depends
from sqlalchemy import select

from src.app_auth.models import User
from src.infrastructure.database.dependencies import get_db_factory
from src.infrastructure.database.factory import DatabaseFactory

router = APIRouter()


@router.get("/token")
async def token(factory: DatabaseFactory = Depends(get_db_factory)):
    async with factory.get_session("default") as session:
        # 使用 session 进行数据库操作
        result = await session.execute(select(User))
        items = result.scalars().all()
        print(items)
    return {"message": "Hello World"}


# # 使用SQLAlchemy特定依赖
# @router.get("/users/sqlalchemy")
# async def get_items_sqlalchemy(
#         db: AsyncSession = Depends(get_db_session)
# ):
#     # query = select(User)
#     # result = await db.execute(query)
#     # user = result.scalar_one_or_none()
#     # return
#     try:
#         result = await db.execute(select(User))
#         items = result.scalars().all()
#         # await db.commit()
#         return items
#     except Exception as e:
#         await db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

#
# @router.get("/items")
# async def get_items(db=Depends(get_db_session)):
#     async with db as session:
#         # 使用会话
#         result = await session.execute(select(User))
#         return result.scalars().all()
