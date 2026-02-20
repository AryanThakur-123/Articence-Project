from typing import List, Dict, Any


class VoiceOptimizer:
    """
    Optimizes responses for voice conversations.
    Reduces payload size and generates summaries.
    """

    MAX_VOICE_RECORDS = 5

    @staticmethod
    def optimize(
        source: str,
        data: List[Dict[str, Any]]
    ) -> tuple[List[Dict[str, Any]], str]:
        """
        Returns:
        - optimized_data
        - voice_summary
        """

        if not data:
            return data, "No results found."

        # Limit records for voice bandwidth
        trimmed_data = data[:VoiceOptimizer.MAX_VOICE_RECORDS]

        if source == "crm":
            return VoiceOptimizer._crm_voice(trimmed_data)

        if source == "support":
            return VoiceOptimizer._support_voice(trimmed_data)

        if source == "analytics":
            return VoiceOptimizer._analytics_voice(trimmed_data)

        return trimmed_data, f"Showing {len(trimmed_data)} records."

    # -------------------------
    # CRM Voice
    # -------------------------
    @staticmethod
    def _crm_voice(data: List[Dict[str, Any]]):
        simplified = [
            {
                "name": c.get("name"),
                "company": c.get("company"),
                "lifetime_value": c.get("lifetime_value"),
            }
            for c in data
        ]

        top = simplified[0]
        summary = (
            f"Top customer is {top['name']} "
            f"from {top['company']} "
            f"with lifetime value {top['lifetime_value']}. "
            f"Showing {len(simplified)} customers."
        )

        return simplified, summary

    # -------------------------
    # Support Voice
    # -------------------------
    @staticmethod
    def _support_voice(data: List[Dict[str, Any]]):
        simplified = [
            {
                "subject": t.get("subject"),
                "priority": t.get("priority"),
                "status": t.get("status"),
            }
            for t in data
        ]

        critical = sum(
            1 for t in simplified if t["priority"] == "critical"
        )

        summary = (
            f"There are {len(simplified)} active tickets. "
            f"{critical} are critical priority."
        )

        return simplified, summary

    # -------------------------
    # Analytics Voice
    # -------------------------
    @staticmethod
    def _analytics_voice(data: List[Dict[str, Any]]):
        latest = data[-1]
        metric = latest.get("metric_name", "metric")
        value = latest.get("value")

        summary = f"The latest value of {metric} is {value}."

        return data, summary
