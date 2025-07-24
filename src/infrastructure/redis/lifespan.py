from src.infrastructure.redis.redis_client import get_redis_manager, RedisManager


# def init_redis(app: FastAPI) -> None:
#     """
#     Creates connection pool for redis.
#
#     :param app: current fastapi application.
#     """
#     app.state.redis_pool = ConnectionPool.from_url(
#         str(settings.redis_url),
#     )
#
#
# async def shutdown_redis(app: FastAPI) -> None:
#     """
#     Closes redis connection pool.
#
#     :param app: current FastAPI app.
#     """
#     await app.state.redis_pool.disconnect()


# @app.on_event("startup")
async def startup_redis():
    # 初始化所有配置的 Redis 连接池
    for redis_id in settings.REDIS_HOSTS:
        get_redis_manager(redis_id)


# @app.on_event("shutdown")
async def shutdown_redis():
    # 关闭所有 Redis 连接池
    for manager in RedisManager._instances.values():
        for connection in manager._pool._created_connections:
            connection.disconnect()
        manager._pool.disconnect()

# from redis import asyncio as redis
#
#
# redis_client = redis.from_url(url=f"redis://{settings.redis_url}", decode_responses=True)
# await redis_client.get

