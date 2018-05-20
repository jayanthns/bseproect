from datetime import timedelta
from celery.schedules import crontab

CELERYBEAT_SCHEDULE = {
    #  Download file script every day at 5.30 am
    "something": {
        "task": "srapper.main1",
        "schedule": crontab(hour=5, minute=30),
        "args": []
    }
}