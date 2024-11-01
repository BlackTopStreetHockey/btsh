from datetime import date, datetime
from zoneinfo import ZoneInfo


def format_datetime(dt: datetime | date, fmt: str = '%m/%d/%Y'):
    return dt.strftime(fmt)


def datetime_to_drf(dt: datetime, tz: str = None):
    """Format a datetime so it matches how django rest framework formats it"""
    as_tz = dt.astimezone(ZoneInfo(tz)) if tz else dt
    value = as_tz.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value
