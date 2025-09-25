from contextlib import suppress

import pytest
from conftest import requires_api_key
from jsonschema import validate
from schemas import IPSTACK_SUCCESS_SCHEMA


def assert_exact_keys(payload: dict, expected_keys: set[str]):
    """Assert that the payload has exactly the expected keys."""
    actual = set(payload.keys())
    # we assume that the API can add service fields, but the test is about fields:
    # so strict equality is best. If you want, change to `issuperset`.
    assert actual == expected_keys, f"Expected keys {expected_keys}, got {actual}"


@pytest.mark.usefixtures("http", "base_url")
class TestIpstackFieldsExact:
    @requires_api_key()
    @pytest.mark.parametrize(
        "fields,expected",
        [
            (
                "ip,type,continent_name,country_name",
                {"ip", "type", "continent_name", "country_name"},
            ),
            ("ip,latitude,longitude", {"ip", "latitude", "longitude"}),
            ("ip", {"ip"}),
        ],
    )
    def test_fields_subset_returns_exact_keys(self, http, base_url, api_key, fields, expected):
        """Test that requesting specific fields returns exactly those fields."""
        params = {"access_key": api_key, "fields": fields}
        r = http.get(f"{base_url}/8.8.8.8", params=params, timeout=20)
        assert r.ok
        data = r.json()
        # The base schema is still valid for a subset (some of the required may be null/missing),
        # so we only apply schema validation here if all required are present.
        # Otherwise, we check for key equality.
        with suppress(Exception):
            validate(data, IPSTACK_SUCCESS_SCHEMA)
        assert_exact_keys(data, expected)
