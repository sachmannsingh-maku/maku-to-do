from celery import Celery

celery_app = Celery(
    "maku_todo",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)



celery_app.autodiscover_tasks(["maku_todo.tasks"])
