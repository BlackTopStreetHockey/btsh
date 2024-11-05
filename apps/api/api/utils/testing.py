from datetime import datetime

import pytest
from rest_framework.reverse import reverse as drf_reverse

from .datetime import datetime_to_drf


@pytest.mark.django_db
class BaseTest:
    def format_datetime(self, dt: datetime, tz: str = None):
        return datetime_to_drf(dt, tz)

    def reverse_api_url(self, *args, url=None, **kwargs):
        url = url or getattr(self, 'url', None)
        return drf_reverse(url, args=args, kwargs=kwargs) if url else None
