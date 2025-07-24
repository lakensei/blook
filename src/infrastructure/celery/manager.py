# infrastructure/celery/config.py
from typing import Optional

from celery import Celery


# celery_app = Celery("worker", broker="amqp://guest@queue//")

# celery_app.conf.task_routes = {"app.worker.test_celery": "main-queue"}

def make_celery(celery_config):
    celery = Celery(
        'worker',
        broker=celery_config.broker_url,
        backend=celery_config.result_backend
    )

    return celery


class CeleryManager:
    def __init__(self):
        print("_________初始化 celery________")
        self._celery = None

    def init_celery(self, broker_url: str, result_backend: str) -> Celery:
        if not self._celery:
            self._celery = Celery(
                'tasks',
                broker=broker_url,
                backend=result_backend
            )
        return self._celery

    def get_celery(self) -> Celery:
        if not self._celery:
            raise RuntimeError("Celery has not been initialized.")
        return self._celery


def create_celery_manager() -> CeleryManager:
    return CeleryManager()


celery_manager: CeleryManager = create_celery_manager()

# 提供一个全局可访问的 Celery 实例
celery_app: Optional[Celery] = None


def get_celery_app() -> Celery:
    global celery_manager
    global celery_app
    if not celery_app:
        # 尝试从 FastAPI app 获取 CeleryManager 并初始化 Celery
        try:
            celery_app = celery_manager.get_celery()
        except ImportError:
            # Celery worker 独立启动的情况
            celery_manager = create_celery_manager()
            from src.common.core.config import settings
            celery_app = celery_manager.init_celery(
                broker_url=settings.celery_config.broker_url,
                result_backend=settings.celery_config.result_backend
            )
    return celery_app


# celery -A infrastructure.celery.manager.celery_app worker --loglevel=info
