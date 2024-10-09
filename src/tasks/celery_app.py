from celery import Celery
from src.config import settings

celery_manager = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=[
        "src.tasks.tasks",
    ],
)

celery_manager.conf.beat_schedule = {
    "luboe-nazvanie": {
        "task": "booking_today_checkin",
        "schedule": 5,
    }
}