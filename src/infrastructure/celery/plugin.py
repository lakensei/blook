from typing import Any, Dict, List, AsyncGenerator, Optional
from contextlib import asynccontextmanager
from celery import Celery
from .dependencies import get_celery
from .tasks import create_celery_app
from ..base import InfrastructurePlugin


class CeleryPlugin(InfrastructurePlugin):
    def __init__(self):
        self._app: Optional[Celery] = None

    @property
    def name(self) -> str:
        return "celery"

    def get_lifespan(self, settings: Dict[str, Any]) -> AsyncGenerator:
        @asynccontextmanager
        async def lifespan():
            # 初始化Celery并配置定时任务
            self._app = create_celery_app(settings)

            # 配置任务路由
            self._app.conf.task_routes = {
                'app.infrastructure.plugins.celery.tasks.*': {'queue': 'default'}
            }

            # 其他Celery配置
            self._app.conf.update(
                task_serializer='json',
                accept_content=['json'],
                result_serializer='json',
                timezone='UTC',
                enable_utc=True,
            )

            yield

            # 清理
            if self._app:
                self._app.control.purge()

        return lifespan()

    def get_provider(self) -> Celery:
        if not self._app:
            raise RuntimeError("Celery not initialized")
        return self._app

    @property
    def dependencies(self) -> List[Any]:
        return [get_celery] 