import datetime
import time
import random


def date_string_to_date(date_str: str = None, delimiter: str = ' '):
    """
    :param date_str: in format 'YYYY-MM-DD' or 'YYYYMMDD' followed with split letter and hour,
                     such as 'YYYY-MM-DD HH:mm:ss' or 'YYYY-MM-DDTHH:mm:ss.zzz',
    :param delimiter: a letter to split date and time, usually as ' ' or 'T'
    :return: datetime.date
    """
    if isinstance(date_str, datetime.date):
        return date_str
    if not date_str:
        ts = now() - datetime.timedelta(hours=9.5)
        return ts.date()
    first_part = date_str.split(delimiter)[0]
    if '-' in first_part:
        return datetime.date.fromisoformat(first_part)
    else:
        first_part = first_part[:4] + '-' + first_part[4:6] + '-' + first_part[6:8]
        return datetime.date.fromisoformat(first_part)


def utcnow():
    return datetime.datetime.utcnow()


def now():
    return datetime.datetime.now()


def today():
    return datetime.date.today()


def get_random_time():
    return datetime.datetime(year=random.randint(1990, 2050),
                             month=random.randint(1, 12),
                             day=random.randint(1, 28))


def get_start_time(range_in_days: int = 1, trunc_mode=0):
    now = datetime.datetime.utcnow()
    end_time = datetime.datetime(now.year, now.month, now.day)
    start_time = end_time - datetime.timedelta(days=range_in_days)
    if trunc_mode < 0:
        return start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    elif trunc_mode > 0:
        dt = start_time + datetime.timedelta(days=1)
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        return start_time
