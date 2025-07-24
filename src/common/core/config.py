from pathlib import Path
from typing import Dict, Any

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(__file__).resolve().parent.parent.parent

CONFIG_PATH = ROOT_PATH.parent.joinpath("conf")
STATIC_PATH = ROOT_PATH.joinpath("static")
LOG_PATH = ROOT_PATH.parent.joinpath("log")  # 日志文件目录
DATA_PATH = ROOT_PATH.parent.joinpath("data")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=CONFIG_PATH.joinpath("dev.env"),
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
    )
    LOG_LEVEL: str = "INFO"
    PROJECT_NAME: str = "blook"
    # 启用的插件列表
    ENABLED_PLUGINS: list[str] = ["database"]

    # 数据库配置
    ORM_TYPE: str = "sqlalchemy"
    DATABASE_URLS: Dict[str, str] = {}

    # Redis配置（可选）
    REDIS_URLS: Dict[str, str] = {}  # str = "redis://localhost:6379"

    # Celery配置
    CELERY_APP_NAME: str = "app"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_CONFIG: Dict[str, Any] = {
        "broker_connection_retry_on_startup": True,
        "worker_prefetch_multiplier": 1,
        "worker_concurrency": 4,
        "worker_max_tasks_per_child": 1000,
        "beat_schedule_filename": "celerybeat-schedule",
        "beat_max_loop_interval": 300,
    }

    # 向量数据库
    VECTOR_TYPE: str = "milvus"
    VECTOR_INFOS: Dict[str, Any] = {}

    # jwt
    ACCESS_TOKEN_EXPIRE_MINUTES: str = ""
    SECRET_KEY: str = ""


settings = Settings()

# 插件配置映射
PLUGIN_SETTINGS = {
    "database": {
        "IMPL_TYPE": settings.ORM_TYPE,
        "DATABASE_URLS": settings.DATABASE_URLS,
    },
    "redis": {
        "REDIS_URLS": settings.REDIS_URLS,
    },
    "celery": {
        "CELERY_APP_NAME": settings.CELERY_APP_NAME,
        "CELERY_BROKER_URL": settings.CELERY_BROKER_URL,
        "CELERY_CONFIG": settings.CELERY_CONFIG,
    },
    "vector": {
        "IMPL_TYPE": settings.VECTOR_TYPE,
        "VECTOR_INFOS": settings.VECTOR_INFOS
    }
}

__all__ = ['settings', 'CONFIG_PATH', 'PLUGIN_SETTINGS', 'LOG_PATH']
