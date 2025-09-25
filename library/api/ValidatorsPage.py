from __future__ import annotations

from collections.abc import Iterable

from IpStackPage import ResponseWrapper


class Validator:
    """Base class for all validators."""

    def validate(self, response: ResponseWrapper) -> None:  # pragma: no cover
        """Validate the response. To be implemented by subclasses."""
        raise NotImplementedError


class StatusCodeIs(Validator):
    """Validator to check if the response status code matches the expected value."""

    def __init__(self, expected: int):
        self.expected = expected

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the response status code matches the expected value."""
        code = response.status_code
        if code != self.expected:
            raise AssertionError(
                f"Status {code} != {self.expected}. Body: {response.response.text[:400]}"
            )


class HeaderStartsWith(Validator):
    """Validator to check if a specific header starts with a given prefix."""

    def __init__(self, header: str, prefix: str):
        self.header = header
        self.prefix = prefix

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the specified header starts with the given prefix."""
        actual = response.headers.get(self.header, "")
        if not actual.startswith(self.prefix):
            raise AssertionError(
                f"Header {self.header}='{actual}' does not start with '{self.prefix}'"
            )


class IsJSON(Validator):
    """Validator to check if the response is in JSON format."""

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the response is in JSON format."""
        ctype = response.headers.get("Content-Type", "")
        if "json" not in ctype:
            raise AssertionError(f"Content-Type is not JSON: {ctype}")
        _ = response.json()


class JsonFieldEquals(Validator):
    """Validator to check if a specific JSON field equals the expected value."""

    def __init__(self, field: str, expected):
        self.field = field
        self.expected = expected

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the specified JSON field equals the expected value."""
        data = response.json()
        actual = data.get(self.field)
        if actual != self.expected:
            raise AssertionError(f"JSON['{self.field}'] == {actual}, expected {self.expected}")


class JsonHasKeys(Validator):
    """Validator to check if the JSON response contains specific keys."""

    def __init__(self, keys: Iterable[str]):
        self.keys = list(keys)

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the JSON response contains the specified keys."""
        data = response.json()
        missing = [k for k in self.keys if k not in data]
        if missing:
            raise AssertionError(
                f"Missing JSON keys: {missing}. Got keys: {list(data.keys())[:30]}"
            )


class JsonExactKeys(Validator):
    """Validator to check if the JSON response contains exactly the specified keys."""

    def __init__(self, keys: Iterable[str]):
        self.keys = sorted(list(keys))

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the JSON response contains exactly the specified keys."""
        data = response.json()
        actual = sorted(list(data.keys()))
        if actual != self.keys:
            raise AssertionError(f"JSON keys {actual} != expected {self.keys}")


class IsXML(Validator):
    """Validator to check if the response is in XML format."""

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the response is in XML format."""
        ctype = response.headers.get("Content-Type", "")
        if "xml" not in ctype:
            raise AssertionError(f"Content-Type is not XML: {ctype}")


class ContentContains(Validator):
    """Validator to check if the response content contains specific byte sequences."""

    def __init__(self, needles: Iterable[bytes]):
        self.needles = list(needles)

    def validate(self, response: ResponseWrapper) -> None:
        """Validate that the response content contains all specified byte sequences."""
        body = response.content
        missing = [n for n in self.needles if n not in body]
        if missing:
            raise AssertionError(f"Response content does not contain: {missing}")
