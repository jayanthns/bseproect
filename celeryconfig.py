from celery.schedules import crontab
from scrapper import app


app.conf.beat_schedule = {
    "something": {
        'task': 'srapper.main1',
        'schedule': crontab(hour=12, minute=30),  # Run every day at 6 PM (UTC TIME)
    },
}
