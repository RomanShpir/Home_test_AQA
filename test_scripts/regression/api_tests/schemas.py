# JSON Schemas for basic IPstack responses (simplified and stable).
# You can extend if needed (e.g., for enterprise fields).

IPSTACK_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["ip", "type", "continent_name", "country_name", "latitude", "longitude"],
    "properties": {
        "ip": {"type": "string"},
        "type": {"type": "string", "enum": ["ipv4", "ipv6"]},
        "continent_name": {"type": ["string", "null"]},
        "country_name": {"type": ["string", "null"]},
        "region_name": {"type": ["string", "null"]},
        "city": {"type": ["string", "null"]},
        "zip": {"type": ["string", "null"]},
        "latitude": {"type": ["number", "null"]},
        "longitude": {"type": ["number", "null"]},
        "location": {"type": ["object", "null"]},
    },
    "additionalProperties": True,
}

# IPstack error format (generalized).
IPSTACK_ERROR_SCHEMA = {
    "type": "object",
    "required": ["success", "error"],
    "properties": {
        "success": {"type": "boolean", "enum": [False]},
        "error": {
            "type": "object",
            "required": ["code", "type", "info"],
            "properties": {
                "code": {"type": "integer"},
                "type": {"type": "string"},
                "info": {"type": "string"},
            },
            "additionalProperties": True,
        },
    },
    "additionalProperties": True,
}
