from datetime import datetime

import pytest

from .datetime import datetime_to_drf


@pytest.mark.django_db
class BaseTest:
    def format_datetime(self, dt: datetime):
        return datetime_to_drf(dt)
