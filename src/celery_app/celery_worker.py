from celery import Celery
from src.core.config import settings


def make_celery():
    app = Celery('tasks', broker=settings.redis_settings.get_rd_url())
    app.autodiscover_tasks(['src.celery_app.tasks'])
    return app


celery: Celery = make_celery()
