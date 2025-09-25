import time

import pytest
from conftest import requires_api_key
from jsonschema import validate
from schemas import IPSTACK_ERROR_SCHEMA


def assert_ipstack_error(resp, *, expected_type_substr: str | None = None):
    """Helper to assert IPstack error response structure and optionally type substring."""
    validate(resp, IPSTACK_ERROR_SCHEMA)
    if expected_type_substr:
        assert expected_type_substr in resp["error"]["type"]


@pytest.mark.usefixtures("http", "base_url")
class TestIpstackNegative:
    def test_invalid_api_key(self, http, base_url, invalid_key):
        """Test response with an invalid API key."""
        r = http.get(f"{base_url}/8.8.8.8", params={"access_key": invalid_key}, timeout=20)
        # IPstack often returns 200 with the success=False field
        assert r.status_code in (200, 401, 403)
        data = r.json()
        if isinstance(data, dict) and data.get("success") is False:
            assert_ipstack_error(data, expected_type_substr="invalid_access_key")
        else:
            # if the provider returned a direct 401/403 with a different body — we accept it as negative
            assert r.status_code in (401, 403)

    @requires_api_key()
    @pytest.mark.skip(reason="Demo test: rate-limit should not be created intentionally in CI")
    def test_rate_limit(self, http, base_url, api_key):
        """Demo test to hit the rate limit by making many requests in a short time."""
        # Note: This test is mostly illustrative. Hitting real rate limits in CI is not ideal.
        # If you want to run it locally, ensure your plan has a low rate limit
        # and adjust the number of requests and intervals accordingly.
        # The free plan has a limit of 250 requests/month and 10k requests/month for the basic plan.
        # Here we do 120 requests with a short delay to try to trigger the limit.
        # If you want to check locally, reduce the intervals and increase the number of calls
        errors = 0
        for _ in range(120):
            r = http.get(f"{base_url}/8.8.8.8", params={"access_key": api_key}, timeout=20)
            if r.status_code == 429 or (r.ok and r.json().get("success") is False):
                errors += 1
                break
            time.sleep(0.2)
        assert errors >= 1, "Expected to hit rate limit at least once"
