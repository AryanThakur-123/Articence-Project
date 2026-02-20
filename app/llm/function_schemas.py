QUERY_DATA_FUNCTION = {
    "name": "query_data",
    "description": "Query structured business data from CRM, Support, or Analytics systems.",
    "parameters": {
        "type": "object",
        "properties": {
            "source": {
                "type": "string",
                "enum": ["crm", "support", "analytics"],
                "description": "The data source to query."
            },
            "filters": {
                "type": "object",
                "description": "Filtering conditions such as metric_name, status, priority, lifetime_value__gt, etc.",
                "additionalProperties": {
                    "type": ["string", "number", "boolean"]
                }
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of results to return.",
                "default": 5
            },
            "offset": {
                "type": "integer",
                "description": "Pagination offset.",
                "default": 0
            },
            "voice_context": {
                "type": "boolean",
                "description": "Whether to optimize the response for voice interaction.",
                "default": False
            }
        },
        "required": ["source"]
    }
}
