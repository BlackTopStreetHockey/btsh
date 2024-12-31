from datetime import datetime

import pytest
from rest_framework.reverse import reverse as drf_reverse

from .datetime import datetime_to_drf


@pytest.mark.django_db
class BaseTest:
    def format_datetime(self, dt: datetime, tz: str = None):
        return datetime_to_drf(dt, tz)

    def format_created_by_updated_by(self, user):
        return user.id

    def reverse_api_url(self, *args, url=None, **kwargs):
        url = url or getattr(self, 'url', None)
        return drf_reverse(url, args=args, kwargs=kwargs) if url else None

    # Create
    def test_create_permission(self, *args, **kwargs):
        ...

    def test_create_valid(self, *args, **kwargs):
        ...

    def test_create_invalid(self, *args, **kwargs):
        ...

    # Retrieve
    def test_retrieve_permission(self, *args, **kwargs):
        ...

    def test_retrieve(self, *args, **kwargs):
        ...

    # Update
    def test_update_permission(self, *args, **kwargs):
        ...

    def test_update_valid(self, *args, **kwargs):
        ...

    def test_update_invalid(self, *args, **kwargs):
        ...

    # Delete
    def test_delete_permission(self, *args, **kwargs):
        ...

    def test_delete_valid(self, *args, **kwargs):
        ...

    def test_delete_invalid(self, *args, **kwargs):
        ...

    # List
    def test_list_permission(self, *args, **kwargs):
        ...

    def test_list(self, *args, **kwargs):
        ...
