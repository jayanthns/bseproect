from celery.schedules import crontab
from scrapper import app


app.conf.beat_schedule = {
    "something": {
        'task': 'scrapper.main1',
        'schedule': crontab(hour=12, minute=15),  # Run every day at 6 PM (UTC TIME)
    },
}
