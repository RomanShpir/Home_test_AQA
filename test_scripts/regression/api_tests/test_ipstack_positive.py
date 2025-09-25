import pytest
from conftest import requires_api_key
from jsonschema import validate
from schemas import IPSTACK_SUCCESS_SCHEMA


@pytest.mark.usefixtures("http", "base_url")
class TestIpstackPositive:
    @requires_api_key()
    def test_lookup_public_ip_ok(self, http, base_url, api_key):
        """Lookup a known public IP and validate the response schema and content."""
        # Let's take 8.8.8.8 as a stable example
        params = {"access_key": api_key}
        r = http.get(f"{base_url}/8.8.8.8", params=params, timeout=20)
        assert r.status_code in (200, 304)
        data = r.json()
        validate(instance=data, schema=IPSTACK_SUCCESS_SCHEMA)
        # sanity checks
        assert data["ip"] in ("8.8.8.8", "8.8.4.4", "8.8.8.8/8") or "8.8." in data["ip"]

    @requires_api_key()
    @pytest.mark.parametrize(
        "ip",
        ["1.1.1.1", "208.67.222.222", "151.101.1.69"],  # Cloudflare, OpenDNS, Fastly
    )
    def test_lookup_various_ips_ok(self, http, base_url, api_key, ip):
        """Lookup various known public IPs and validate the response schema."""
        params = {"access_key": api_key}
        r = http.get(f"{base_url}/{ip}", params=params, timeout=20)
        assert r.ok
        validate(r.json(), IPSTACK_SUCCESS_SCHEMA)
