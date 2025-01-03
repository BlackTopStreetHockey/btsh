def clean_data(data: dict, ignore_keys: list[str] = None) -> dict:
    """
    Removes the given dict keys present in serializer/response data so they aren't included in the assertion.

    By default removes the common fields created_by, updated_by, created_at, updated_at. These fields aren't vital to
    test and have made testing a bit more annoying/brittle. For example created_at and updated_at require timezone
    conversions that cause tests to periodically fail when run by themselves vs part of the full test suite.
    """
    ignore_keys = ignore_keys or ['created_by', 'updated_by', 'created_at', 'updated_at']

    for k in ignore_keys:
        data.pop(k, None)
    return data


def assert_data(data: dict, expected_data: dict, ignore_keys: list[str] = None):
    """Asserts serializer data or response data matches the expected data."""
    assert clean_data(data, ignore_keys) == expected_data
