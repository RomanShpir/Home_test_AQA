import os

import pytest
import requests

BASE_URL = os.getenv("IPSTACK_BASE_URL", "http://api.ipstack.com")
VALID_KEY = os.getenv("IPSTACK_API_KEY")
INVALID_KEY = os.getenv("IPSTACK_INVALID_KEY", "foo")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL for the API."""
    return BASE_URL.rstrip("/")


@pytest.fixture(scope="session")
def api_key() -> str | None:
    """Valid API key for the API."""
    return VALID_KEY


@pytest.fixture(scope="session")
def invalid_key() -> str:
    """Invalid API key for the API."""
    return INVALID_KEY


@pytest.fixture(scope="session")
def http():
    """HTTP session for making requests."""
    with requests.Session() as s:
        s.headers.update({"User-Agent": "Home_test_AQA/pytest"})
        yield s


def requires_api_key():
    """Skip test if no valid API key is provided."""
    return pytest.mark.skipif(not VALID_KEY, reason="Set IPSTACK_API_KEY to run integration tests.")
