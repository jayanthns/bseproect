from datetime import timedelta
from celery.schedules import crontab
from srapper import app
app.conf.timezone = 'Asia/Kolkata'
app.conf.beat_schedule = {
    "something": {
        'task': 'srapper.main1',
        'schedule': crontab(hour=18, minute=27),

    },
}

# CELERYBEAT_SCHEDULE = {
#     #  Download file script every day at 5.30 am
#     "something": {
#         "task": "srapper.main1",
#         "schedule": crontab(minute=8, hour=11),
#         "args": []
#     }
# }

# Command to run celery beat
# celery -A srapper worker -B --loglevel=INFO