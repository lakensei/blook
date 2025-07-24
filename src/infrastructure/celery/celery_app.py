from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Dict, Any

from celery import Celery

from src.common.core.config import PLUGIN_SETTINGS
from src.infrastructure.container import InfrastructureContainer


def create_celery_app(settings: Dict[str, Any]) -> Celery:
    app = Celery(
        settings["CELERY_APP_NAME"],
        broker=settings["CELERY_BROKER_URL"]
    )

    # # 配置定时任务
    # app.conf.beat_schedule = {
    #     'sync-user-data-every-hour': {
    #         'task': 'app.infrastructure.plugins.celery.tasks.sync_user_data',
    #         'schedule': crontab(minute=0, hour='*'),  # 每小时执行
    #     },
    #     'daily-report-generation': {
    #         'task': 'app.infrastructure.plugins.celery.tasks.generate_daily_report',
    #         'schedule': crontab(minute=0, hour=0),  # 每天凌晨执行
    #     },
    #     'cleanup-expired-data': {
    #         'task': 'app.infrastructure.plugins.celery.tasks.cleanup_expired_data',
    #         'schedule': crontab(minute=0, hour=2),  # 每天凌晨2点执行
    #     }
    # }

    return app


async def initialize_database():
    """初始化数据库连接"""
    from src.infrastructure.database.config import DatabasesConfig
    db_plugin = InfrastructureContainer.get_plugin("database")
    config = DatabasesConfig.from_settings(PLUGIN_SETTINGS["database"])
    await db_plugin.get_provider().initialize(config)


async def cleanup_database():
    """清理数据库连接"""
    db_plugin = InfrastructureContainer.get_plugin("database")
    await db_plugin.get_provider().cleanup()


@asynccontextmanager
async def managed_db_session(db_name: str = "default"):
    """管理数据库会话的上下文管理器"""
    try:
        # 初始化数据库连接
        await initialize_database()

        # 获取数据库会话
        from ..database.dependencies import get_db_session
        async for session in get_db_session(db_name):
            yield session

    finally:
        # 清理数据库连接
        await cleanup_database()


# 定义任务
@get_celery_app().task
@task_logging
async def sync_user_data():
    """同步用户数据的定时任务"""
    try:
        async with managed_db_session("system", "default") as db_session:
            # 执行同步操作
            current_time = datetime.utcnow()
            print(f"Syncing user data at {current_time}")
            # ... 同步逻辑
            await db_session.commit()
    except Exception as e:
        print(f"Error syncing user data: {e}")
        raise


@get_celery_app().task
@task_logging
async def generate_daily_report(report_date: str):
    """生成每日报告的定时任务"""
    try:
        # 获取Redis连接
        redis = InfrastructureContainer.get_plugin("redis").get_provider()

        async with managed_db_session("business", "default") as db_session:
            # 生成报告
            report_date = datetime.utcnow().date()
            print(f"Generating daily report for {report_date}")

            # 从数据库获取数据
            # ... 报告生成逻辑

            # 将报告缓存到Redis
            report_key = f"daily_report:{report_date}"
            await redis.set(report_key, "report_data", ex=86400)  # 24小时过期

            await db_session.commit()
    except Exception as e:
        print(f"Error generating daily report: {e}")
        raise


@get_celery_app().task
async def cleanup_expired_data():
    """清理过期数据的定时任务"""
    try:
        async with managed_db_session("system", "default") as db_session:
            cutoff_date = datetime.utcnow() - timedelta(days=30)
            print(f"Cleaning up data older than {cutoff_date}")

            # 清理过期数据
            # ... 清理逻辑

            await db_session.commit()
    except Exception as e:
        print(f"Error cleaning up expired data: {e}")
        raise
