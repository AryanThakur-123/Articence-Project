from typing import List, Dict, Any


def identify_data_type(data: List[Dict[str, Any]]) -> str:
    """
    Identify structure of returned data.
    Returns: tabular | time-series | aggregated | hierarchical | unknown
    """

    if not data:
        return "unknown"

    sample = data[0]

    # Time-series detection
    if "timestamp" in sample and "value" in sample:
        return "time_series"

    # Aggregated metric detection (single metric value)
    if len(data) == 1 and "value" in sample:
        return "aggregated"

    # Hierarchical detection (nested structures)
    for value in sample.values():
        if isinstance(value, dict) or isinstance(value, list):
            return "hierarchical"

    # Default
    return "tabular"

