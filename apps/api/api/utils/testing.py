from datetime import datetime

import pytest


@pytest.mark.django_db
class BaseTest:
    def format_datetime(self, dt: datetime):
        """Format a datetime so it matches how django rest framework format"""
        value = dt.isoformat()
        if value.endswith('+00:00'):
            value = value[:-6] + 'Z'
        return value
