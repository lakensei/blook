# @app.on_event("startup")
from .manager import celery_app


async def startup_event(celery_config: dict):
    # 初始化 Celery 并应用环境变量中的配置
    celery_app.conf.update(celery_config)
