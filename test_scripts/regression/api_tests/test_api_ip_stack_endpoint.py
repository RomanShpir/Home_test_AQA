import pytest
from main_api import Api
from ValidatorsPage import (
    StatusCodeIs, IsJSON, JsonHasKeys, JsonFieldEquals, JsonExactKeys,
    IsXML, HeaderStartsWith, ContentContains
)

# ---- STANDARD LOOKUP CASES ----
standard_cases = [
    pytest.param(
        {"ip": "134.201.250.155", "kwargs": {}},
        # validators
        [
            StatusCodeIs(200),
            IsJSON(),
            JsonFieldEquals("ip", "134.201.250.155"),
            JsonHasKeys(["country_name"]),
        ],
        id="standard-basic",
    ),
    pytest.param(
        {"ip": "160.39.144.19", "kwargs": {"hostname": 1}},
        [
            StatusCodeIs(200),
            IsJSON(),
            JsonFieldEquals("ip", "160.39.144.19"),
            JsonHasKeys(["hostname"]),
        ],
        id="standard-hostname",
    ),
    pytest.param(
        {"ip": "134.201.250.155", "kwargs": {"language": "ru"}},
        [
            StatusCodeIs(200),
            IsJSON(),
            JsonFieldEquals("ip", "134.201.250.155"),
            JsonHasKeys(["country_name"]),
        ],
        id="standard-language-ru",
    ),
    pytest.param(
        {"ip": "134.201.250.155", "kwargs": {"fields": "zip"}},
        [
            StatusCodeIs(200),
            IsJSON(),
            JsonExactKeys(["zip"]),
        ],
        id="standard-fields-zip",
    ),
    pytest.param(
        {"ip": "160.39.144.19", "kwargs": {"output": "xml"}},
        [
            StatusCodeIs(200),
            IsXML(),
            HeaderStartsWith("Content-Type", "application/xml"),
            ContentContains([b"<ip>", b"</ip>"]),
        ],
        id="standard-xml",
    ),
]

@pytest.mark.parametrize("case, validators", standard_cases)
def test_standard_lookup_param_clean(api: Api, case, validators):
    """Test standard_lookup with various parameters and validate the responses."""

    response = api.ip_stack.standard_lookup(case["ip"], **case["kwargs"])
    response.check(*validators)


# TODO: Commented out as the bulk lookup feature is not available in the current subscription plan.
# # ---- BULK LOOKUP CASES ----
# bulk_cases = [
#     pytest.param(
#         {"ips": ["72.229.28.185", "110.174.165.78"], "kwargs": {}},
#         [
#             StatusCodeIs(200),
#             IsJSON(),
#             ContentContains([]),
#         ],
#         id="bulk-basic",
#     ),
#     pytest.param(
#         {"ips": ["72.229.28.185", "110.174.165.78"], "kwargs": {"hostname": 1}},
#         [
#             StatusCodeIs(200),
#             IsJSON(),
#         ],
#         id="bulk-hostname",
#     ),
# ]
#
# @pytest.mark.parametrize("case, validators", bulk_cases)
# def test_bulk_lookup_param_clean(ipstack, case, validators):
#     """Test bulk_lookup with various parameters and validate the responses."""
#
#     resp = ipstack.bulk_lookup(case["ips"], **case["kwargs"])
#     resp.check(*validators)
