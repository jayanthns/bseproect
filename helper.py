from datetime import datetime, timedelta
import redis

"""
Week days 0 is Monday, so 6 is Sunday
If day is 5(Saturday) get friday with substract 1 day
Similar for sunday substract 2 days
"""
WEEK_DAY = (('Mon', 0, 0), ('Tue', 1, 0), ('Wed', 2, 0), ('Thu', 3, 0), ('Fri', 4, 0), ('Sat', 5, 1), ('Sun', 6, 2))
# (('Mon': 0), ('Tue': 0), ('Wed': 0), ('Thu': 0), ('Fri': 0), ('Sat': 1), ('Sun': 2))


def get_date_str(minus_day):
    today = datetime.now() - timedelta(days=minus_day)
    today = today - timedelta(days=(day[2] for day in WEEK_DAY if day[1] == today.weekday()).next())
    date_str = today.strftime("%d%m%y")
    return date_str


def get_redis_connection():
    return redis.Redis('localhost', port=6379, db=0)


def get_sorted_list(result, type):
    if type == 'dict':
        result = sorted(result, key=lambda x: (x['open'], x['high'], x['low'], x['close']))
        result = result[::-1]
    return result
