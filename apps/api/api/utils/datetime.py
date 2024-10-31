from datetime import date, datetime


def format_datetime(dt: datetime | date, fmt: str = '%m/%d/%Y'):
    return dt.strftime(fmt)


def datetime_to_drf(dt: datetime):
    """Format a datetime so it matches how django rest framework formats it"""
    value = dt.isoformat()
    if value.endswith('+00:00'):
        value = value[:-6] + 'Z'
    return value
