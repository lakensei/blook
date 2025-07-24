from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from celery import Celery
from celery.schedules import crontab
from importlib import import_module
from app.infrastructure.models.system.task import TaskDefinition, TaskLog
from app.infrastructure.plugins.database.base import BaseCRUD, BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

class TaskManager:
    def __init__(self, celery_app: Celery, repository: BaseRepository):
        self.celery_app = celery_app
        self.repository = repository
        self.task_crud: BaseCRUD = repository.get_crud(TaskDefinition)
        self.log_crud: BaseCRUD = repository.get_crud(TaskLog)

    async def register_task(self, task_def: Dict[str, Any]) -> TaskDefinition:
        """注册新任务"""
        task = await self.task_crud.create(task_def)
        await self.reload_schedule()
        return task

    async def update_task(self, task_id: int, data: Dict[str, Any]) -> Optional[TaskDefinition]:
        """更新任务配置"""
        task = await self.task_crud.update(task_id, data)
        if task:
            await self.reload_schedule()
        return task

    async def delete_task(self, task_id: int) -> bool:
        """删除任务"""
        success = await self.task_crud.delete(task_id)
        if success:
            await self.reload_schedule()
        return success

    async def get_task_logs(
        self,
        task_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[TaskLog]:
        """获取任务执行日志"""
        filters = {}
        if task_id:
            filters["task_id"] = task_id
        if start_date:
            filters["start_time__gte"] = start_date
        if end_date:
            filters["start_time__lte"] = end_date
        if status:
            filters["status"] = status

        return await self.log_crud.get_filtered(
            filters=filters,
            skip=0,
            limit=limit,
            order_by=[("-start_time", True)]  # True表示降序
        )

    async def reload_schedule(self):
        """重新加载任务调度"""
        # 获取所有启用的任务
        tasks = await self.task_crud.get_filtered(
            filters={"enabled": True}
        )

        # 清除现有调度
        self.celery_app.conf.beat_schedule = {}

        # 重新加载调度
        for task in tasks:
            schedule = self._parse_schedule(task.schedule)
            if schedule:
                self.celery_app.conf.beat_schedule[f'task-{task.id}'] = {
                    'task': task.task_path,
                    'schedule': schedule,
                    'args': task.args,
                    'kwargs': task.kwargs,
                    'options': {
                        'task_id': f'task-{task.id}-{datetime.utcnow().timestamp()}'
                    }
                }

    def _parse_schedule(self, schedule_config: Dict) -> Any:
        """解析调度配置"""
        schedule_type = schedule_config.get('type')
        
        if schedule_type == 'cron':
            return crontab(**schedule_config['config'])
        elif schedule_type == 'interval':
            return timedelta(**schedule_config['config'])
        elif schedule_type == 'one_off':
            return schedule_config['config']['datetime']
        return None

    async def log_task_start(self, task_id: int, celery_task_id: str) -> TaskLog:
        """记录任务开始"""
        log_data = {
            "task_id": task_id,
            "celery_task_id": celery_task_id,
            "status": "STARTED",
            "start_time": datetime.utcnow()
        }
        return await self.log_crud.create(log_data)

    async def log_task_end(
        self,
        celery_task_id: str,
        status: str,
        result: Optional[str] = None,
        error: Optional[str] = None
    ) -> Optional[TaskLog]:
        """记录任务结束"""
        logs = await self.log_crud.get_filtered(
            filters={"celery_task_id": celery_task_id},
            limit=1
        )
        if logs:
            log = logs[0]
            end_time = datetime.utcnow()
            update_data = {
                "status": status,
                "result": result,
                "error": error,
                "end_time": end_time,
                "duration": int((end_time - log.start_time).total_seconds())
            }
            return await self.log_crud.update(log.id, update_data)
        return None 