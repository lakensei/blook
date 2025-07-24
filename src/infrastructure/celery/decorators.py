# from functools import wraps
# from datetime import datetime
# from app.infrastructure.container import InfrastructureContainer
#
# def task_logging(func):
#     """任务日志装饰器"""
#     @wraps(func)
#     async def wrapper(*args, **kwargs):
#         task_id = int(func.request.id.split('-')[1])
#         celery_task_id = func.request.id
#
#         # 获取任务管理器
#         db_plugin = InfrastructureContainer.get_plugin("database")
#         async with db_plugin.get_session() as session:
#             task_manager = TaskManager(func.app, session)
#
#             try:
#                 # 记录任务开始
#                 await task_manager.log_task_start(task_id, celery_task_id)
#
#                 # 执行任务
#                 result = await func(*args, **kwargs)
#
#                 # 记录任务成功
#                 await task_manager.log_task_end(
#                     celery_task_id,
#                     'SUCCESS',
#                     str(result)
#                 )
#                 return result
#
#             except Exception as e:
#                 # 记录任务失败
#                 await task_manager.log_task_end(
#                     celery_task_id,
#                     'FAILURE',
#                     error=str(e)
#                 )
#                 raise
#     return wrapper