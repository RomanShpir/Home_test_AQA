from __future__ import annotations
import requests
from requests.structures import CaseInsensitiveDict


class ResponseWrapper:
    """A wrapper around requests.Response to provide additional functionality."""
    def __init__(self, response: requests.Response):
        self._response = response

    @property
    def response(self) -> requests.Response:
        return self._response

    def json(self):
        return self._response.json()

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def headers(self) -> CaseInsensitiveDict[str]:
        return self._response.headers

    @property
    def content(self) -> bytes:
        return self._response.content

    def check(self, *validators) -> "ResponseWrapper":
        for v in validators:
            v.validate(self)
        return self  # fluent


class IpStackPage:
    """Client for the ipstack API."""

    def __init__(self, base_url: str, access_key: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.params = {"access_key": access_key}

    def standard_lookup(self, ip: str, *, hostname: int = 0,
                        language: str | None = None,
                        fields: str | None = None,
                        output: str | None = None) -> ResponseWrapper:
        """
        Perform a standard IP lookup with optional parameters.

        :param ip: IP address to look up.
        :param hostname: Whether to include the hostname in the response (0 or 1).
        :param language: Language for the response (e.g., 'en', 'ru').
        :param fields: Comma-separated list of fields to include in the response.
        :param output: Output format ('json' or 'xml').
        :return: ResponseWrapper containing the API response.
        """
        params: dict = {}
        if hostname:
            params["hostname"] = hostname
        if language:
            params["language"] = language
        if fields:
            params["fields"] = fields
        if output:
            params["output"] = output
        r = self.session.get(f"{self.base_url}/{ip}", params=params)
        return ResponseWrapper(r)

    def bulk_lookup(self, ips: list[str], *, hostname: int = 0) -> ResponseWrapper:
        """
        Perform a bulk IP lookup for multiple IP addresses.

        :param ips: List of IP addresses to look up.
        :param hostname: Whether to include the hostname in the response (0 or 1).
        :return: ResponseWrapper containing the API response.
        """
        params: dict = {}
        if hostname:
            params["hostname"] = hostname
        ip_str = ",".join(ips)
        r = self.session.get(f"{self.base_url}/{ip_str}", params=params)
        return ResponseWrapper(r)
