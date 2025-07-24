from celery import Celery

from src.infrastructure.container import InfrastructureContainer


def get_celery() -> Celery:
    return InfrastructureContainer.get_plugin("celery").get_provider()
