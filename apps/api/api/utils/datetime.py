from datetime import date, datetime


def format_datetime(dt: datetime | date, fmt: str = '%m/%d/%Y'):
    return dt.strftime(fmt)
